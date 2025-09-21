from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Text, DateTime, Index
from datetime import datetime
from app.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class TranslationLog(Base):
    __tablename__ = "translation_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    translation_id = Column(String(50), unique=True, index=True)
    original_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=False)
    source_language = Column(String(10), nullable=False)
    target_language = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_agent = Column(String(500))
    ip_address = Column(String(45))
    
    # Add indexes for better query performance
    __table_args__ = (
        Index('idx_created_at', 'created_at'),
        Index('idx_target_language', 'target_language'),
    )

def create_tables():
    """Create database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Database dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()