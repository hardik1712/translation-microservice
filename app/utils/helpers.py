import re
from typing import Optional

def is_valid_language_code(language_code: str) -> bool:
    """Validate language code format"""
    # Check if it's a valid 2-3 character language code
    pattern = r'^[a-z]{2,3}$'
    return bool(re.match(pattern, language_code.lower()))

def sanitize_text(text: str) -> str:
    """Sanitize input text"""
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove potentially harmful characters (basic sanitization)
    text = re.sub(r'[<>]', '', text)
    
    return text

def validate_text_length(text: str, max_length: int = 1000) -> bool:
    """Validate text length"""
    return len(text) <= max_length
