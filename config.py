import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOAD_FOLDER = os.path.join('instance', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'xlsx', 'xls'}