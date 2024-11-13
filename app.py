from converter import excel_to_json, json_to_pdf

excel_file_path = 'recruiters.xlsx'
table_header = ["Recruiters", "Cabinets", "LinkedIn", "Mail"]
attrs = ["Recruteurs", "Cabinets", "LinkedIn", "Mail Pylote"]

json_data = excel_to_json(excel_file_path, attrs)
pdf_output_path = 'output.pdf'

result = json_to_pdf(json_data, pdf_output_path, table_header, attrs)
if 'error' in result:
    print(f'Error: {result["error"]}')
else:
    print(f'Success! PDF report generated at {pdf_output_path}')