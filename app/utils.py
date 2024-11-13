import os
from werkzeug.utils import secure_filename
from flask import current_app

def get_base_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_uploaded_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return filepath
    return None