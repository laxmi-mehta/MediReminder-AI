"""
Fixed API views with correct response format for frontend.
"""
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

from .models import Prescription, PrescriptionItem
from .serializers import PrescriptionSerializer
from ai.ocr_service import extract_text_from_image, parse_prescription_text
from ai.exceptions import (
    OCRProcessingError, 
    PrescriptionParsingError,
    InvalidImageError,
    UnsupportedFileTypeError
)

logger = logging.getLogger(__name__)


class OCRUploadView(APIView):
    """API endpoint for prescription image upload and OCR processing."""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    def post(self, request):
        """Handle prescription image upload with OCR processing."""
        logger.info(f"OCR upload request from user: {request.user.username}")
        
        if 'image' not in request.FILES:
            logger.warning(f"Upload attempt without image file by {request.user.username}")
            return Response(
                {"success": False, "error": "No image file provided. Please upload an image."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        image_file = request.FILES['image']
        logger.info(f"Processing image: {image_file.name} ({image_file.size} bytes)")
        
        if image_file.size > self.MAX_FILE_SIZE:
            logger.warning(f"File size {image_file.size} exceeds limit")
            return Response(
                {"success": False, "error": f"File size exceeds {self.MAX_FILE_SIZE // (1024*1024)}MB limit."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            self._validate_image(image_file)
        except (UnsupportedFileTypeError, InvalidImageError) as e:
            logger.warning(f"Image validation failed: {e}")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        prescription = None
        
        try:
            prescription = Prescription.objects.create(user=request.user, image=image_file)
            logger.info(f"Created prescription #{prescription.id}")
            
            try:
                raw_text = extract_text_from_image(prescription.image.path)
                logger.info(f"Extracted text length: {len(raw_text)}")
            except OCRProcessingError as e:
                logger.error(f"OCR extraction failed: {e}")
                prescription.delete()
                return Response(
                    {
                        "success": False,
                        "error": "Failed to extract text from image. Please ensure the image is clear and readable.",
                        "details": str(e) if request.user.is_staff else None
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            try:
                parsed_data = parse_prescription_text(raw_text)
            except PrescriptionParsingError as e:
                logger.error(f"Parsing failed: {e}")
                return Response(
                    {
                        "success": False,
                        "error": "Failed to parse prescription details.",
                        "prescription_id": prescription.id,
                        "details": str(e) if request.user.is_staff else None
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            if parsed_data.get('doctor_name'):
                prescription.doctor_name = parsed_data['doctor_name']
                prescription.save()
                logger.info(f"Updated doctor name: {prescription.doctor_name}")
            
            medications_created = []
            for med in parsed_data.get('medications', []):
                if med.get('name'):
                    try:
                        prescription_item = PrescriptionItem.objects.create(
                            prescription=prescription,
                            medication_name=med['name'],
                            dosage=med.get('dosage'),
                            frequency=med.get('frequency')
                        )
                        medications_created.append({
                            "name": prescription_item.medication_name,
                            "dosage": prescription_item.dosage,
                            "frequency": prescription_item.frequency
                        })
                        logger.debug(f"Created medication: {prescription_item.medication_name}")
                    except Exception as e:
                        logger.error(f"Failed to create medication: {e}")
            
            logger.info(f"Successfully processed prescription #{prescription.id} with {len(medications_created)} medications")
            
            response_data = {
                "success": True,
                "message": "Prescription uploaded and processed successfully.",
                "prescription_id": prescription.id,
                "doctor_name": prescription.doctor_name,
                "medications": medications_created,
                "medications_count": len(medications_created)
            }
            
            if not medications_created:
                logger.warning(f"No medications extracted for prescription #{prescription.id}")
                response_data["warning"] = "No medications could be extracted. Please verify the image quality."
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            if prescription:
                prescription.delete()
            return Response(
                {
                    "success": False,
                    "error": "An unexpected error occurred.",
                    "details": str(e) if request.user.is_staff else None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _validate_image(self, image_file: InMemoryUploadedFile):
        """Validate uploaded image file."""
        file_extension = image_file.name.split('.')[-1].lower()
        if file_extension not in self.ALLOWED_EXTENSIONS:
            raise UnsupportedFileTypeError("Invalid file type", allowed_types=self.ALLOWED_EXTENSIONS)
        
        try:
            img = Image.open(image_file)
            img.verify()
            image_file.seek(0)
        except Exception as e:
            logger.error(f"Image validation failed: {e}")
            raise InvalidImageError("Invalid or corrupted image file")


class PrescriptionListView(APIView):
    """
    FIXED: Returns array directly instead of paginated response.
    API endpoint to retrieve user's prescription history.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get all prescriptions for authenticated user - returns array directly."""
        try:
            logger.info(f"Fetching prescriptions for user: {request.user.username}")
            prescriptions = Prescription.objects.filter(user=request.user)
            serializer = PrescriptionSerializer(
                prescriptions, 
                many=True,
                context={'request': request}
            )
            logger.info(f"Returning {prescriptions.count()} prescriptions")
            
            # Return array directly for frontend compatibility
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error fetching prescriptions: {e}", exc_info=True)
            return Response(
                {"success": False, "error": "Failed to retrieve prescriptions."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PrescriptionDetailView(APIView):
    """API endpoint to retrieve specific prescription by ID."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, prescription_id):
        """Get details of a specific prescription."""
        try:
            logger.info(f"Fetching prescription #{prescription_id} for {request.user.username}")
            prescription = Prescription.objects.get(id=prescription_id, user=request.user)
            serializer = PrescriptionSerializer(prescription, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Prescription.DoesNotExist:
            logger.warning(f"Prescription #{prescription_id} not found")
            return Response(
                {"success": False, "error": "Prescription not found or access denied."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error fetching prescription: {e}", exc_info=True)
            return Response(
                {"success": False, "error": "Failed to retrieve prescription."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )