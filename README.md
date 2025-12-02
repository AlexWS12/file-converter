# # WIP

# File Converter Tool

Author: Alex Waisman

A lightweight Python application for converting between multiple file formats including CSV, JSON, Markdown, HTML, and NumPy arrays.

## Features

- **Supported Conversions:**
  - CSV ↔ JSON ↔ NPY ↔ YAML
  - Markdown ↔ HTML
  - PDF ↔ HTML
  - Image ↔ WebP
  - PNG ↔ JPEG
  - TXT ↔ PDF
  - TXT ↔ DOCX
  - JSON ↔ TOON
  - And more (soon)

- **Web Interface:** User-friendly Streamlit UI for uploading and converting files
- **Modular Design:** Conversion logic organized by file type pairs

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AlexWS12/file-convertor.git
   cd file-convertor
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

Then:
1. Select source and target file formats
2. Upload your file
3. Click "Convert"
4. Download the converted file

## Project Structure

- `app.py` - Streamlit web interface
- `converter.py` - Main conversion logic
- `conversions/` - Individual conversion modules
- `uploaded_files/` - Temporary storage for processed files

## Requirements

- Python 3.7+
- numpy, pillow, reportlab, python-docx, pydub, streamlit

## License

MIT License
