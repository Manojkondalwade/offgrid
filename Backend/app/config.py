import os

class Config:
    SECRET_KEY              = os.getenv('SECRET_KEY', 'dev-secret-key')
    JWT_SECRET_KEY          = os.getenv('JWT_SECRET_KEY', 'dev-jwt-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///offgrid.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production':  ProductionConfig,
    'default':     DevelopmentConfig,
}