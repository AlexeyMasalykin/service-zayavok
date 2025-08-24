from .base import BaseConfig
import os

class ProductionConfig(BaseConfig):
    DEBUG = False
    
    # Безопасность
    SECRET_KEY = os.getenv("SECRET_KEY")
    
    # База данных (можно использовать PostgreSQL для продакшена)
    # DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
    
    # SSL и безопасность
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Логирование
    LOG_LEVEL = 'INFO'
    
    # Домен для CORS (если нужно)
    ALLOWED_HOSTS = ['v412372.hosted-by-vdsina.com', 'localhost']