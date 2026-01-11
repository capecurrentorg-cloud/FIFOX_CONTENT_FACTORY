"""
Configuration management for FIFOX Backend
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///fifox.db')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    
    # Toast POS API
    TOAST_POS_API_KEY = os.getenv('TOAST_POS_API_KEY', '')
    TOAST_POS_API_URL = os.getenv('TOAST_POS_API_URL', 'https://api.toasttab.com')
    
    # Vapi.ai API
    VAPI_API_KEY = os.getenv('VAPI_API_KEY', '')
    VAPI_API_URL = os.getenv('VAPI_API_URL', 'https://api.vapi.ai')
    
    # Google Maps API
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')
    
    # Social Media APIs
    INSTAGRAM_TOKEN = os.getenv('INSTAGRAM_TOKEN', '')
    FACEBOOK_TOKEN = os.getenv('FACEBOOK_TOKEN', '')
    TIKTOK_API_KEY = os.getenv('TIKTOK_API_KEY', '')
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', '')
    SNAPCHAT_API_KEY = os.getenv('SNAPCHAT_API_KEY', '')
    
    # OpenAI for content generation
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # WebSocket Configuration
    SOCKETIO_ASYNC_MODE = 'eventlet'
    SOCKETIO_CORS_ALLOWED_ORIGINS = CORS_ORIGINS
    
    # Mock mode (for development/demo)
    USE_MOCK_DATA = os.getenv('USE_MOCK_DATA', 'True').lower() == 'true'


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    USE_MOCK_DATA = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    USE_MOCK_DATA = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
