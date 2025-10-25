import os
import logging
import platform
import shutil

from django.conf import settings

from PIL import Image, ImageFilter, ImageOps
import pytesseract
import re
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

#Not used in the project
def _configure_tesseract_binary() -> None:
    tess_cmd = getattr(settings, 'TESSERACT_CMD', '') or os.getenv('TESSERACT_CMD', '')
    if tess_cmd:
        pytesseract.pytesseract.tesseract_cmd = tess_cmd
        logger.debug('Using TESSERACT_CMD from configuration: %s', tess_cmd)
        return

    # Try to find tesseract on PATH first
    found_on_path = shutil.which('tesseract')
    if found_on_path:
        pytesseract.pytesseract.tesseract_cmd = found_on_path
        logger.debug('Found tesseract on PATH: %s', found_on_path)
        return

    # Probe common Windows install locations
    if platform.system().lower() == 'windows':
        candidate_paths = [
            r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe",
            r"C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe",
            r"C:\\Users\\%USERNAME%\\scoop\\apps\\tesseract\\current\\tesseract.exe",
            r"C:\\ProgramData\\chocolatey\\bin\\tesseract.exe",
        ]
        expanded_candidates = [os.path.expandvars(p) for p in candidate_paths]
        for path in expanded_candidates:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                logger.debug('Detected tesseract at: %s', path)
                return

    logger.warning('TESSERACT_CMD not set and tesseract not found. Please install and/or set TESSERACT_CMD')

#Not used in the project
def _preprocess_image(image: Image.Image) -> Image.Image:

    max_dim = 1800
    width, height = image.size
    scale = min(max_dim / max(width, height), 1.0)
    if scale < 1.0:
        new_size = (int(width * scale), int(height * scale))
        image = image.resize(new_size, Image.LANCZOS)

    image = image.convert('L')

    image = ImageOps.autocontrast(image)

    image = image.filter(ImageFilter.MedianFilter(size=3))

    image = ImageOps.invert(image)
    image = ImageOps.autocontrast(image)
    image = ImageOps.invert(image)

    threshold = 150
    image = image.point(lambda x: 255 if x > threshold else 0, mode='1')

    return image


def extract_text_from_image(image_path: str) -> str:
    try:
        _configure_tesseract_binary()

        if not image_path:
            logger.warning('extract_prescription_data called with empty image_path')
            return ""

        if not os.path.exists(image_path):
            logger.warning('Image path does not exist: %s', image_path)
            return ""

        with Image.open(image_path) as img:
            processed = _preprocess_image(img)

            custom_oem_psm_config = "--oem 3 --psm 6"
            try:
                # Sanity check to surface tesseract availability issues early
                _ = pytesseract.get_tesseract_version()
            except Exception as version_err:
                logger.warning('Tesseract not available or misconfigured: %s', version_err)
                return ""

            text = pytesseract.image_to_string(
                processed,
                config=custom_oem_psm_config,
                lang=os.getenv('TESSERACT_LANG', 'eng')
            )

            if not text:
                logger.info('Tesseract returned no text for image: %s', image_path)
                return ""

            return text.strip()
    except Exception as exc:
        logger.exception('OCR extraction failed: %s', exc)
        return ""



def parse_prescription_text(raw_text: str) -> Dict:
    """
    Parse raw OCR text from a prescription image into structured data.
    
    Args:
        raw_text (str): Raw text extracted from prescription image
        
    Returns:
        dict: Structured prescription data with doctor_name and medications list
        
    Example:
        {
            "doctor_name": "Dr. Sharma",
            "medications": [
                {"name": "Paracetamol", "dosage": "500mg", "frequency": "2 times/day"}
            ]
        }
    """
    if not raw_text or not raw_text.strip():
        return {"doctor_name": None, "medications": []}
    
    # Normalize text: remove extra whitespace and standardize line breaks
    text = re.sub(r'\s+', ' ', raw_text)
    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
    
    # Initialize result structure
    result = {
        "doctor_name": None,
        "medications": []
    }
    
    # Extract doctor name
    result["doctor_name"] = _extract_doctor_name(text, lines)
    
    # Extract medications
    result["medications"] = _extract_medications(text, lines)
    
    return result


def _extract_doctor_name(text: str, lines: List[str]) -> Optional[str]:
    """
    Extract doctor name from prescription text.
    Looks for patterns like "Dr.", "Dr ", "Doctor", etc.
    """
    # Pattern 1: "Dr. Name" or "Dr Name" or "DR. NAME"
    doctor_patterns = [
        r'(?:Dr\.?|DR\.?|Doctor)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        r'(?:Dr\.?|DR\.?|Doctor)\s+([A-Z]+(?:\s+[A-Z]+)*)',
    ]
    
    for pattern in doctor_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return f"Dr. {match.group(1).strip()}"
    
    # Pattern 2: Look in first few lines for names with "Dr" prefix
    for line in lines[:5]:
        if re.search(r'\bdr\.?\b', line, re.IGNORECASE):
            # Extract capitalized words after "Dr"
            words = line.split()
            dr_index = next((i for i, w in enumerate(words) 
                           if re.match(r'dr\.?', w, re.IGNORECASE)), None)
            if dr_index is not None and dr_index + 1 < len(words):
                name_parts = []
                for word in words[dr_index + 1:]:
                    if word[0].isupper() and word.isalpha():
                        name_parts.append(word)
                    else:
                        break
                if name_parts:
                    return f"Dr. {' '.join(name_parts)}"
    
    return None


def _extract_medications(text: str, lines: List[str]) -> List[Dict[str, Optional[str]]]:
    """
    Extract medication information from prescription text.
    Looks for medication names, dosages, and frequency patterns.
    """
    medications = []
    
    # Common dosage patterns
    dosage_pattern = r'\b(\d+\.?\d*\s*(?:mg|g|ml|mcg|units?|tablet?s?|cap(?:sule)?s?|tab))\b'
    
    # Frequency patterns
    frequency_patterns = [
        r'\b(\d+\s*(?:time?s?|x)\s*(?:per|/|a)?\s*day)\b',
        r'\b(once|twice|thrice)\s*(?:daily|a day|per day)?\b',
        r'\b(morning|evening|night|afternoon)\b',
        r'\b(before|after)\s*(?:meals?|food|breakfast|lunch|dinner)\b',
        r'\b(every\s+\d+\s*hours?)\b',
        r'\b(OD|BD|TDS|QDS)\b',  # Medical abbreviations
    ]
    
    # Keywords that often indicate start of medication list
    med_section_keywords = ['prescribed', 'medications?', 'medicines?', 'drugs?', 'rx', 'treatment']
    
    # Find where medication list likely starts
    start_index = 0
    for i, line in enumerate(lines):
        if any(re.search(rf'\b{keyword}\b', line, re.IGNORECASE) for keyword in med_section_keywords):
            start_index = i + 1
            break
    
    # Process lines that likely contain medications
    relevant_lines = lines[start_index:]
    
    for line in relevant_lines:
        # Skip very short lines or lines with only numbers
        if len(line) < 3 or line.isdigit():
            continue
        
        # Skip lines that look like headers or instructions
        if re.search(r'^(note|instruction|direction|warning)', line, re.IGNORECASE):
            continue
        
        medication = {
            "name": None,
            "dosage": None,
            "frequency": None
        }
        
        # Extract dosage
        dosage_match = re.search(dosage_pattern, line, re.IGNORECASE)
        if dosage_match:
            medication["dosage"] = dosage_match.group(1).strip()
        
        # Extract frequency
        for freq_pattern in frequency_patterns:
            freq_match = re.search(freq_pattern, line, re.IGNORECASE)
            if freq_match:
                medication["frequency"] = freq_match.group(0).strip()
                break
        
        # Extract medication name (words before dosage or at start of line)
        # Remove dosage and frequency from line to isolate name
        name_line = line
        if dosage_match:
            name_line = name_line[:dosage_match.start()].strip()
        
        # Clean up medication name
        # Remove common prefixes like numbers, bullets, "Tab.", "Cap.", etc.
        name_line = re.sub(r'^[\d\.\)\-\*]+\s*', '', name_line)
        name_line = re.sub(r'^(?:tab\.?|cap\.?|syrup|injection|inj\.?)\s*', '', name_line, flags=re.IGNORECASE)
        
        # Get the first meaningful word(s) as medication name
        words = name_line.split()
        if words:
            # Take first 1-3 capitalized words as medication name
            med_name_parts = []
            for word in words[:3]:
                if word and (word[0].isupper() or word.isalpha()):
                    med_name_parts.append(word)
                else:
                    break
            
            if med_name_parts:
                medication["name"] = ' '.join(med_name_parts)
            elif words:
                # Fallback: take first word if no capitalized words found
                medication["name"] = words[0]
        
        # Only add medication if we found at least a name
        if medication["name"] and len(medication["name"]) > 2:
            medications.append(medication)
    
    # Fallback: if no structured medications found, try simple line-by-line extraction
    if not medications:
        for line in relevant_lines[:10]:  # Check first 10 relevant lines
            # Look for lines that start with capital letter and contain some alphanum
            if re.match(r'^[A-Z]', line) and len(line) > 5 and any(c.isalpha() for c in line):
                words = line.split()[:3]
                med_name = ' '.join(w for w in words if w.isalpha() or w[0].isupper())
                
                if med_name and len(med_name) > 2:
                    medications.append({
                        "name": med_name,
                        "dosage": None,
                        "frequency": None
                    })
    
    return medications


