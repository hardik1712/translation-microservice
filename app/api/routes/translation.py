from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.models import (
    TranslationRequest, 
    BulkTranslationRequest,
    TranslationResponse,
    BulkTranslationResponse,
    ErrorResponse
)
from app.database import get_db, TranslationLog
from app.services.translation_service import TranslationService
from app.services.logging_service import LoggingService
from app.utils.helpers import get_client_ip, get_user_agent
from app.core.exceptions import TranslationServiceException, create_http_exception

router = APIRouter(prefix="/api/v1", tags=["Translation"])

@router.post("/translate", response_model=TranslationResponse)
async def translate_text(
    request: TranslationRequest,
    http_request: Request,
    db: Session = Depends(get_db)
):
    """
    Translate a single text
    
    - **text**: Text to translate (max 1000 characters)
    - **target_language**: Target language code (e.g., 'hi', 'ta', 'kn')
    """
    try:
        # Initialize services
        translation_service = TranslationService()
        logging_service = LoggingService(db)
        
        # Perform translation
        result = await translation_service.translate_text(
            text=request.text,
            target_language=request.target_language
        )
        
        # Log the translation
        user_agent = get_user_agent(http_request)
        ip_address = get_client_ip(http_request)
        
        logging_service.log_translation(
            translation_data=result,
            user_agent=user_agent,
            ip_address=ip_address
        )
        
        return TranslationResponse(**result)
        
    except TranslationServiceException as e:
        raise create_http_exception(500, e.message, e.error_code)
    except Exception as e:
        raise create_http_exception(500, f"Internal server error: {str(e)}", "INTERNAL_ERROR")

@router.post("/translate/bulk", response_model=BulkTranslationResponse)
async def translate_bulk_text(
    request: BulkTranslationRequest,
    http_request: Request,
    db: Session = Depends(get_db)
):
    """
    Translate multiple texts in bulk
    
    - **texts**: Array of texts to translate (max 10 items, each max 1000 characters)
    - **target_language**: Target language code (e.g., 'hi', 'ta', 'kn')
    """
    try:
        # Initialize services
        translation_service = TranslationService()
        logging_service = LoggingService(db)
        
        # Perform bulk translation
        result = await translation_service.translate_bulk(
            texts=request.texts,
            target_language=request.target_language
        )
        
        # Log the translations
        user_agent = get_user_agent(http_request)
        ip_address = get_client_ip(http_request)
        
        logging_service.log_bulk_translations(
            translations=result['translations'],
            user_agent=user_agent,
            ip_address=ip_address
        )
        
        return BulkTranslationResponse(**result)
        
    except TranslationServiceException as e:
        raise create_http_exception(500, e.message, e.error_code)
    except Exception as e:
        raise create_http_exception(500, f"Internal server error: {str(e)}", "INTERNAL_ERROR")

@router.get("/translate/logs")
async def get_translation_logs(
    limit: int = Query(default=50, ge=1, le=100, description="Number of logs to retrieve (1-100)"),
    offset: int = Query(default=0, ge=0, description="Number of logs to skip"),
    db: Session = Depends(get_db)
):
    """
    Retrieve translation logs with pagination
    
    - **limit**: Number of logs to retrieve (default: 50, max: 100)
    - **offset**: Number of logs to skip (default: 0)
    """
    try:
        logging_service = LoggingService(db)
        logs = logging_service.get_translation_logs(limit=limit, offset=offset)
        
        return {
            "success": True,
            "logs": [
                {
                    "id": log.id,
                    "translation_id": log.translation_id,
                    "original_text": log.original_text,
                    "translated_text": log.translated_text,
                    "source_language": log.source_language,
                    "target_language": log.target_language,
                    "created_at": log.created_at,
                    "user_agent": log.user_agent,
                    "ip_address": log.ip_address
                }
                for log in logs
            ],
            "total_returned": len(logs),
            "limit": limit,
            "offset": offset,
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        raise create_http_exception(500, f"Failed to retrieve logs: {str(e)}", "LOG_RETRIEVAL_ERROR")