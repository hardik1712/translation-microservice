from fastapi import HTTPException
from typing import Optional

class TranslationServiceException(Exception):
    """Base exception for translation service"""
    def __init__(self, message: str, error_code: Optional[str] = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class TranslationAPIException(TranslationServiceException):
    """Exception for translation API errors"""
    pass

class ValidationException(TranslationServiceException):
    """Exception for validation errors"""
    pass

class DatabaseException(TranslationServiceException):
    """Exception for database errors"""
    pass

def create_http_exception(status_code: int, message: str, error_code: Optional[str] = None):
    """Create HTTP exception with proper format"""
    return HTTPException(
        status_code=status_code,
        detail={
            "success": False,
            "error": message,
            "error_code": error_code
        }
    )