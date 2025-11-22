import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///fixit.db'
    # Default to local MySQL. Format: mysql+pymysql://username:password@host/db_name
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:@localhost/bybytoo'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Add database connection pooling for production
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 299,
        'pool_timeout': 20,
        'pool_pre_ping': True,
        'pool_size': 5,
        'max_overflow': 10
    }