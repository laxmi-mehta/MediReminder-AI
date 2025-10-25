from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import io

from .models import Prescription, PrescriptionItem
from .serializers import PrescriptionSerializer
from ai.ocr_service import extract_text_from_image, parse_prescription_text


class OCRUploadView(APIView):
    """
    API endpoint to upload prescription images, extract text via OCR,
    and parse medication details.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    # Allowed image formats
    ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    def post(self, request):
        """
        Handle prescription image upload and OCR processing.
        
        Expected input:
            - image: Image file (jpg, jpeg, png)
        
        Returns:
            - prescription_id: ID of created prescription
            - doctor_name: Extracted doctor name
            - medications: List of extracted medications with dosage and frequency
        """
        # Validate image file presence
        if 'image' not in request.FILES:
            return Response(
                {"error": "No image file provided. Please upload an image."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        image_file = request.FILES['image']
        
        # Validate file size
        if image_file.size > self.MAX_FILE_SIZE:
            return Response(
                {"error": f"File size exceeds {self.MAX_FILE_SIZE // (1024*1024)}MB limit."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate image type
        validation_error = self._validate_image(image_file)
        if validation_error:
            return Response(
                {"error": validation_error},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Create Prescription instance
            prescription = Prescription.objects.create(
                user=request.user,
                image=image_file
            )
            
            # Extract text from image using OCR
            try:
                raw_text = extract_text_from_image(prescription.image.path)
            except Exception as ocr_error:
                # Delete prescription if OCR fails
                prescription.delete()
                return Response(
                    {
                        "error": "Failed to extract text from image. Please ensure the image is clear and readable.",
                        "details": str(ocr_error)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Parse extracted text into structured data
            try:
                parsed_data = parse_prescription_text(raw_text)
            except Exception as parse_error:
                # Keep prescription but log parsing error
                return Response(
                    {
                        "error": "Failed to parse prescription text. The image was saved but medication details could not be extracted.",
                        "prescription_id": prescription.id,
                        "details": str(parse_error)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Update doctor name if found
            if parsed_data.get('doctor_name'):
                prescription.doctor_name = parsed_data['doctor_name']
                prescription.save()
            
            # Create PrescriptionItem instances for each medication
            medications_created = []
            for med in parsed_data.get('medications', []):
                if med.get('name'):  # Only create if medication name exists
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
            
            # Prepare success response
            response_data = {
                "success": True,
                "message": "Prescription uploaded and processed successfully.",
                "prescription_id": prescription.id,
                "doctor_name": prescription.doctor_name,
                "medications": medications_created,
                "medications_count": len(medications_created)
            }
            
            # Warning if no medications found
            if not medications_created:
                response_data["warning"] = "No medications could be extracted from the prescription. Please verify the image quality."
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(
                {
                    "error": "An unexpected error occurred while processing the prescription.",
                    "details": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _validate_image(self, image_file: InMemoryUploadedFile) -> str:
        """
        Validate uploaded image file.
        
        Args:
            image_file: Uploaded file object
            
        Returns:
            Error message if invalid, None if valid
        """
        # Check file extension
        file_extension = image_file.name.split('.')[-1].lower()
        if file_extension not in self.ALLOWED_EXTENSIONS:
            return f"Invalid file type. Allowed types: {', '.join(self.ALLOWED_EXTENSIONS)}"
        
        # Verify it's actually an image by trying to open with PIL
        try:
            img = Image.open(image_file)
            img.verify()  # Verify it's not corrupted
            
            # Reset file pointer after verification
            image_file.seek(0)
            
        except Exception as e:
            return f"Invalid or corrupted image file. Please upload a valid image."
        
        return None


class PrescriptionListView(APIView):
    """
    API endpoint to retrieve user's prescription history.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get all prescriptions for the authenticated user.
        """
        prescriptions = Prescription.objects.filter(user=request.user)
        serializer = PrescriptionSerializer(
            prescriptions, 
            many=True,
            context={'request': request}
        )
        return Response({
            "count": prescriptions.count(),
            "prescriptions": serializer.data
        }, status=status.HTTP_200_OK)


class PrescriptionDetailView(APIView):
    """
    API endpoint to retrieve a specific prescription by ID.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, prescription_id):
        """
        Get details of a specific prescription.
        """
        try:
            prescription = Prescription.objects.get(
                id=prescription_id,
                user=request.user
            )
            serializer = PrescriptionSerializer(
                prescription,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Prescription.DoesNotExist:
            return Response(
                {"error": "Prescription not found or you don't have permission to access it."},
                status=status.HTTP_404_NOT_FOUND
            )