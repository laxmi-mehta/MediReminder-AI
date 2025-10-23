import os
import logging
import platform
import shutil

from django.conf import settings

from PIL import Image, ImageFilter, ImageOps
import pytesseract

logger = logging.getLogger(__name__)


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


def extract_prescription_data(image_path: str) -> str:
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


