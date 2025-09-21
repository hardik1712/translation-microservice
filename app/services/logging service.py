from typing import List, Optional
from sqlalchemy.orm import Session
from app.database import TranslationLog
from app.core.exceptions import DatabaseException

class LoggingService:
    def __init__(self, db: Session):
        self.db = db
    
    def log_translation(self, translation_data: dict, user_agent: Optional[str] = None, ip_address: Optional[str] = None):
        """Log a single translation request"""
        try:
            log_entry = TranslationLog(
                translation_id=translation_data['translation_id'],
                original_text=translation_data['original_text'],
                translated_text=translation_data['translated_text'],
                source_language=translation_data['source_language'],
                target_language=translation_data['target_language'],
                user_agent=user_agent,
                ip_address=ip_address
            )
            
            self.db.add(log_entry)
            self.db.commit()
            
        except Exception as e:
            self.db.rollback()
            raise DatabaseException(f"Failed to log translation: {str(e)}", "DB_LOG_ERROR")
    
    def log_bulk_translations(self, translations: List[dict], user_agent: Optional[str] = None, ip_address: Optional[str] = None):
        """Log multiple translation requests"""
        try:
            log_entries = []
            for translation in translations:
                if translation.get('success', True):  # Only log successful translations
                    log_entry = TranslationLog(
                        translation_id=translation['translation_id'],
                        original_text=translation['original_text'],
                        translated_text=translation['translated_text'],
                        source_language=translation['source_language'],
                        target_language=translation['target_language'],
                        user_agent=user_agent,
                        ip_address=ip_address
                    )
                    log_entries.append(log_entry)
            
            self.db.add_all(log_entries)
            self.db.commit()
            
        except Exception as e:
            self.db.rollback()
            raise DatabaseException(f"Failed to log bulk translations: {str(e)}", "DB_BULK_LOG_ERROR")
    
    def get_translation_logs(self, limit: int = 50, offset: int = 0) -> List[TranslationLog]:
        """Retrieve translation logs with pagination"""
        try:
            return self.db.query(TranslationLog)\
                         .order_by(TranslationLog.created_at.desc())\
                         .offset(offset)\
                         .limit(limit)\
                         .all()
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve logs: {str(e)}", "DB_RETRIEVE_ERROR")
    