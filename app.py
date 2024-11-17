import click
import json
import os
from app import create_app
from app.converter import ExcelConverter

def run_web_mode(host='127.0.0.1', port=5000, debug=False):
    """Run the application in web mode"""
    app = create_app()
    print(f"Starting web server on {host}:{port}")
    print("Access the application at http://{}:{}".format(host, port))
    app.run(host=host, port=port, debug=debug, use_reloader=True)

def run_cli_mode(input_file, output_file, output_type, pagesize, fontsize, textcolor, backgroundcolor):
    """Run the application in CLI mode"""
    try:
        if not os.path.exists(input_file):
            click.echo(f"Error: Input file '{input_file}' does not exist.", err=True)
            return
        
        click.echo("Processing file...")
        
        # Convert to JSON first
        json_data = ExcelConverter.excel_to_json(input_file)
        
        if isinstance(json_data, dict) and 'error' in json_data:
            click.echo(f"Error: {json_data['error']}", err=True)
            return
        
        if output_type == 'json':
            # Save JSON output
            with open(output_file, 'w') as f:
                json.dump(json.loads(json_data), f, indent=2)
            click.echo(f"Successfully converted to JSON: {output_file}")
        
        else:  # PDF output
            result = ExcelConverter.json_to_pdf(json_data, output_file, pagesize=pagesize, fontsize=fontsize, textcolor=textcolor, backgroundcolor=backgroundcolor)
            if result.get('success'):
                click.echo(f"Successfully converted to PDF: {output_file}")
            else:
                click.echo(f"Error generating PDF: {result.get('error', 'Unknown error')}", err=True)
                
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@click.command()
@click.option('--mode', '-m', 
              type=click.Choice(['web', 'cli']), 
              default='web',
              help='Run in web or CLI mode')
@click.option('--host', '-h', 
              default='127.0.0.1',
              help='Host for web server (web mode only)')
@click.option('--port', '-p', 
              default=5000,
              help='Port for web server (web mode only)')
@click.option('--debug', '-d', 
              is_flag=True,
              help='Enable debug mode (web mode only)')
@click.option('--input', '-i',
              type=click.Path(exists=True),
              help='Input Excel file path (CLI mode only)')
@click.option('--output', '-o',
              type=click.Path(),
              help='Output file path (CLI mode only)')
@click.option('--type', '-t',
              type=click.Choice(['json', 'pdf']),
              default='json',
              help='Output type (CLI mode only)')
@click.option('--pagesize', '-ps', default='A3', help='Page size for PDF output (CLI mode only)')
@click.option('--fontsize', '-fs', default=10, type=int, help='Font size for PDF output (CLI mode only)')
@click.option('--textcolor', '-tc', default='#000000', help='Text color for PDF output (CLI mode only)')
@click.option('--backgroundcolor', '-bc', default='#ffffff', help='Background color for PDF output (CLI mode only)')
def main(mode, host, port, debug, input, output, type, pagesize, fontsize, textcolor, backgroundcolor):
    """Excel Converter - Convert Excel files to JSON or PDF
    
    Run in web mode:
        python app.py --mode web
        
    Run in CLI mode:
        python app.py --mode cli --input file.xlsx --output result.json --type json
    """
    if mode == 'web':
        run_web_mode(host, port, debug)
    else:
        if not input or not output:
            click.echo("Error: In CLI mode, both --input and --output are required.", err=True)
            return
        run_cli_mode(input, output, type, pagesize, fontsize, textcolor, backgroundcolor)

if __name__ == '__main__':
    main()