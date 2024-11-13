import pandas as pd
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def excel_to_json(file_path, attrs):
    try:
        df = pd.read_excel(file_path)
        json_data = df.to_json(orient='records', indent=2)
        return json_data
    except Exception as e:
        return {'error': str(e)}

def json_to_pdf(json_data, pdf_output_path='output.pdf', table_header=[], attrs=[]):
    try:
        data = json.loads(json_data)
        if data:
            doc = SimpleDocTemplate(pdf_output_path, pagesize=A3)
            story = []
            table_data = [table_header]
            for entry in data:
                table_data.append([entry.get(attr, "") for attr in attrs])
            table = Table(table_data)
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), '#77aaff'),
                ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), '#e6f7ff'),
            ])
            table.setStyle(style)
            story.append(table)
            doc.build(story)
            return {'success': True}
        else:
            return {'error': 'JSON data is empty, no PDF file generated.'}
    except Exception as e:
        return {'error': str(e)}
