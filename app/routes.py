import os
from flask import Blueprint, render_template, request, jsonify, send_file, current_app
from app.utils import save_uploaded_file, get_base_path
from app.converter import ExcelConverter
import json

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@bp.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
        
    file = request.files['file']
    output_type = request.form.get('output_type', 'json')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    filepath = save_uploaded_file(file)
    if not filepath:
        return jsonify({'error': 'Invalid file type'}), 400
    
    try:
        # Convert to JSON
        json_data = ExcelConverter.excel_to_json(filepath)
        
        # Remove temporary file
        os.remove(filepath)
        
        if output_type == 'json':
            return jsonify(json.loads(json_data))
         
        # PDF output
        output_name = os.path.splitext(file.filename)[0] + '.pdf'
        pdf_path = os.path.join(get_base_path(), current_app.config['UPLOAD_FOLDER'], output_name)
        result = ExcelConverter.json_to_pdf(json_data, pdf_path)
        
        if result.get('success'):
            return send_file(pdf_path, as_attachment=True)
        else:
            return jsonify({'error': 'PDF generation failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500