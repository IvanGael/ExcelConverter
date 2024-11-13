import pandas as pd
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Spacer
import datetime

class ExcelConverter:
    @staticmethod
    def excel_to_json(file_path, attrs=None):
        try:
            df = pd.read_excel(file_path)
            if attrs:
                df = df[attrs]
            json_data = df.to_json(orient='records', indent=2)
            return json_data
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def json_to_pdf(json_data, pdf_output_path='output.pdf', table_header=None, attrs=None):
        try:
            data = json.loads(json_data) if isinstance(json_data, str) else json_data
            
            if not data:
                return {'error': 'No data to convert'}
            
            if not attrs:
                attrs = list(data[0].keys())
            
            if not table_header:
                table_header = attrs
            
            doc = SimpleDocTemplate(
                pdf_output_path,
                pagesize=A3,
                rightMargin=30,
                leftMargin=30,
                topMargin=30,
                bottomMargin=30
            )
            
            story = []
            
            # Title and metadata
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30
            )
            
            title = Paragraph("Data Report", title_style)
            story.append(title)
            
            # Timestamp
            timestamp = Paragraph(
                f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                styles["Normal"]
            )
            story.append(timestamp)
            story.append(Spacer(1, 20))
            
            # Create table
            table_data = [table_header]
            for entry in data:
                table_data.append([str(entry.get(attr, "")) for attr in attrs])
            
            table = Table(table_data)
            
            # Table style
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f9ff')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ])
            table.setStyle(style)
            
            story.append(table)
            doc.build(story)
            return {'success': True}
            
        except Exception as e:
            return {'error': str(e)}