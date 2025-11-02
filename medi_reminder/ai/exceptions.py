"""
Custom exceptions for OCR and prescription parsing operations.
"""


class OCRProcessingError(Exception):
    """
    Raised when OCR text extraction fails.
    """
    def __init__(self, message="Failed to extract text from image", original_error=None):
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)
    
    def __str__(self):
        if self.original_error:
            return f"{self.message}: {str(self.original_error)}"
        return self.message


class PrescriptionParsingError(Exception):
    """
    Raised when prescription text parsing fails.
    """
    def __init__(self, message="Failed to parse prescription data", original_error=None):
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)
    
    def __str__(self):
        if self.original_error:
            return f"{self.message}: {str(self.original_error)}"
        return self.message


class InvalidImageError(Exception):
    """
    Raised when uploaded file is not a valid image.
    """
    def __init__(self, message="Invalid or corrupted image file"):
        self.message = message
        super().__init__(self.message)


class UnsupportedFileTypeError(Exception):
    """
    Raised when uploaded file type is not supported.
    """
    def __init__(self, message="Unsupported file type", allowed_types=None):
        self.message = message
        self.allowed_types = allowed_types
        super().__init__(self.message)
    
    def __str__(self):
        if self.allowed_types:
            return f"{self.message}. Allowed types: {', '.join(self.allowed_types)}"
        return self.message