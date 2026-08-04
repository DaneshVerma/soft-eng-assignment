import os

class Config:
    """Base configuration containing defaults and common settings."""
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "dev-secret-key-must-be-long-enough")
    JWT_SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY", "super-secret-jwt-key-that-is-at-least-32-bytes-long")
    SQLALCHEMY_DATABASE_URI: str = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    DEBUG: bool = False
    TESTING: bool = False

class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing environment configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    
class ProductionConfig(Config):
    """Production environment configuration."""
    pass
