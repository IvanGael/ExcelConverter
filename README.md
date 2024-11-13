# Excel Converter

Excel Converter is an app that allows users to convert Excel files to JSON or PDF format. It can be run in both web and CLI modes.

![Demo](https://github.com/user-attachments/assets/dd1f5a09-16a3-4f27-a13b-e76a424e199b)

## Features

- Upload Excel files and convert them to JSON or PDF.
- Download the converted files directly from the web interface.
- Run the application in CLI mode for batch processing.

## Install
```sh
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

## Run
* web mode (default)
```sh
python app.py
# or explicitly
python app.py --mode web
# with custom host and port
python app.py --mode web --host 0.0.0.0 --port 8000
# with debug mode
python app.py --mode web --debug
```

* CLI mode
```sh
# Convert to JSON
python app.py --mode cli --input data.xlsx --output result.json --type json

# Convert to PDF
python app.py --mode cli --input data.xlsx --output result.pdf --type pdf
```