import uuid
from typing import List, Optional
from datetime import datetime
from googletrans import Translator
from app.core.exceptions import TranslationAPIException
from app.config import get_settings

settings = get_settings()

class TranslationService:
    def __init__(self):
        self.translator = Translator() if not settings.USE_MOCK_TRANSLATION else None
        
        # Mock translations for demo purposes
        self.mock_translations = {
            'hi': {
                'hello': 'नमस्ते',
                'how are you': 'आप कैसे हैं',
                'good morning': 'सुप्रभात',
                'thank you': 'धन्यवाद',
                'goodbye': 'अलविदा'
            },
            'ta': {
                'hello': 'வணக்கம்',
                'how are you': 'எப்படி இருக்கீங்க',
                'good morning': 'காலை வணக்கம்',
                'thank you': 'நன்றி',
                'goodbye': 'பிரியாவிடை'
            },
            'kn': {
                'hello': 'ನಮಸ್ಕಾರ',
                'how are you': 'ನೀವು ಹೇಗಿದ್ದೀರಿ',
                'good morning': 'ಶುಭೋದಯ',
                'thank you': 'ಧನ್ಯವಾದಗಳು',
                'goodbye': 'ವಿದಾಯ'
            },
            'bn': {
                'hello': 'হ্যালো',
                'how are you': 'আপনি কেমন আছেন',
                'good morning': 'শুভ সকাল',
                'thank you': 'ধন্যবাদ',
                'goodbye': 'বিদায়'
            }
        }
    
    async def translate_text(self, text: str, target_language: str, source_language: Optional[str] = None) -> dict:
        """
        Translate a single text
        
        Args:
            text: Text to translate
            target_language: Target language code
            source_language: Source language code (optional)
            
        Returns:
            Dictionary containing translation result
        """
        try:
            translation_id = str(uuid.uuid4())
            
            if settings.USE_MOCK_TRANSLATION:
                translated_text, detected_language = await self._mock_translate(text, target_language)
            else:
                translated_text, detected_language = await self._google_translate(
                    text, target_language, source_language
                )
            
            return {
                'success': True,
                'original_text': text,
                'translated_text': translated_text,
                'source_language': detected_language,
                'target_language': target_language,
                'translation_id': translation_id,
                'timestamp': datetime.utcnow()
            }
            
        except Exception as e:
            raise TranslationAPIException(f"Translation failed: {str(e)}", "TRANSLATION_ERROR")
    
    async def translate_bulk(self, texts: List[str], target_language: str) -> dict:
        """
        Translate multiple texts
        
        Args:
            texts: List of texts to translate
            target_language: Target language code
            
        Returns:
            Dictionary containing bulk translation results
        """
        translations = []
        
        for text in texts:
            try:
                result = await self.translate_text(text, target_language)
                translations.append(result)
            except Exception as e:
                # Continue with other translations even if one fails
                translations.append({
                    'success': False,
                    'original_text': text,
                    'translated_text': '',
                    'source_language': 'unknown',
                    'target_language': target_language,
                    'translation_id': str(uuid.uuid4()),
                    'timestamp': datetime.utcnow(),
                    'error': str(e)
                })
        
        return {
            'success': True,
            'translations': translations,
            'total_translations': len(translations),
            'timestamp': datetime.utcnow()
        }
    
    async def _mock_translate(self, text: str, target_language: str) -> tuple:
        """Mock translation for demo purposes"""
        text_lower = text.lower().strip()
        
        if target_language in self.mock_translations:
            # Check for exact matches first
            if text_lower in self.mock_translations[target_language]:
                return self.mock_translations[target_language][text_lower], 'en'
            
            # Check for partial matches
            for key, value in self.mock_translations[target_language].items():
                if key in text_lower:
                    return text.replace(key, value, 1), 'en'
        
        # If no translation found, return a formatted response
        return f"[{target_language.upper()}] {text}", 'en'
    
    async def _google_translate(self, text: str, target_language: str, source_language: Optional[str] = None) -> tuple:
        """Google Translate API translation"""
        if not self.translator:
            raise TranslationAPIException("Google Translator not initialized", "TRANSLATOR_ERROR")
        
        try:
            result = self.translator.translate(
                text,
                dest=target_language,
                src=source_language
            )
            
            return result.text, result.src
            
        except Exception as e:
            raise TranslationAPIException(f"Google Translate error: {str(e)}", "GOOGLE_API_ERROR")