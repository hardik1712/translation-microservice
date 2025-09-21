from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

# Supported language codes
SUPPORTED_LANGUAGES = {
    'en', 'hi', 'ta', 'kn', 'bn', 'te', 'ml', 'gu', 'mr', 'pa', 'or', 'as',
    'fr', 'es', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh', 'ar', 'th', 'vi'
}

class TranslationRequest(BaseModel):
    text: str = Field(..., max_length=1000, description="Text to translate (max 1000 characters)")
    target_language: str = Field(..., description="Target language ISO code (e.g., 'hi', 'ta', 'kn')")
    
    @validator('text')
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError('Text cannot be empty')
        if len(v) > 1000:
            raise ValueError('Text exceeds maximum length of 1000 characters')
        return v.strip()
    
    @validator('target_language')
    def validate_language(cls, v):
        if v.lower() not in SUPPORTED_LANGUAGES:
            raise ValueError(f'Unsupported language code: {v}')
        return v.lower()

class BulkTranslationRequest(BaseModel):
    texts: List[str] = Field(..., max_items=10, description="List of texts to translate (max 10 items)")
    target_language: str = Field(..., description="Target language ISO code")
    
    @validator('texts')
    def validate_texts(cls, v):
        if not v:
            raise ValueError('Texts list cannot be empty')
        if len(v) > 10:
            raise ValueError('Maximum 10 texts allowed per bulk request')
        
        for i, text in enumerate(v):
            if not text or not text.strip():
                raise ValueError(f'Text at index {i} cannot be empty')
            if len(text) > 1000:
                raise ValueError(f'Text at index {i} exceeds maximum length of 1000 characters')
        
        return [text.strip() for text in v]
    
    @validator('target_language')
    def validate_language(cls, v):
        if v.lower() not in SUPPORTED_LANGUAGES:
            raise ValueError(f'Unsupported language code: {v}')
        return v.lower()

class TranslationResponse(BaseModel):
    success: bool
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    translation_id: str
    timestamp: datetime

class BulkTranslationResponse(BaseModel):
    success: bool
    translations: List[TranslationResponse]
    total_translations: int
    timestamp: datetime

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    service: str
    version: str

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    error_code: Optional[str] = None
    timestamp: datetime