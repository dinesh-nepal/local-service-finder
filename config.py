# import os
# from urllib.parse import quote_plus

# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
#      # MySQL Configuration
#     MYSQL_HOST = 'localhost'
#     MYSQL_USER = 'lsf_user'
#     MYSQL_PASSWORD = 'localservicefinder@20'  
#     MYSQL_DB = 'lsf_db'
#     # MYSQL_HOST = os.environ.get('MYSQL_HOST')
#     # MYSQL_USER = os.environ.get('MYSQL_USER')
#     # MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
#     # MYSQL_DB = os.environ.get('MYSQL_DB')
    
#     ENCODED_PASSWORD=quote_plus(MYSQL_PASSWORD)

#     SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{MYSQL_USER}:{ENCODED_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
    
#     UPLOAD_FOLDER = 'static/images/uploads'
#     MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
#     ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


#     # Session Configuration - 3 days
#     PERMANENT_SESSION_LIFETIME = 259200  # 3 days in seconds
#     SESSION_COOKIE_SECURE = False  # in production it should be set true with https
#     SESSION_COOKIE_HTTPONLY = True
#     SESSION_COOKIE_SAMESITE = 'Lax'


import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

class Config:
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database Configuration
    # For local development
    if os.environ.get('DATABASE_URL'):
        # Production (Render uses DATABASE_URL)
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
        if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
            SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    else:
        # Local MySQL
        MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
        MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
        MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'password')
        MYSQL_DB = os.environ.get('MYSQL_DB', 'lsf_db')
        ENCODED_PASSWORD=quote_plus(MYSQL_PASSWORD)
        SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{MYSQL_USER}:{ENCODED_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload Configuration
    UPLOAD_FOLDER = 'static/images/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = 259200  # 3 days
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'