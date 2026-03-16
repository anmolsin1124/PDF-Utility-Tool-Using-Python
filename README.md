# PDF Utility Tool

A browser-based PDF Utility Tool built with **Streamlit** and Python. It helps users convert PDF files into images, convert images into PDF files, and merge multiple PDF files into one.

## Features

- **PDF to Images** – Upload a PDF and download each page as a JPEG image (with preview).
- **Images to PDF** – Upload multiple images and combine them into a single PDF.
- **Merge PDFs** – Upload multiple PDF files and merge them into one.

## Project Structure

```
project/
├── app.py              # Streamlit web application
├── project.py          # Original CLI tool (preserved for reference)
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/anmolsin1124/PDF-Utility-Tool-Using-Python.git
   cd PDF-Utility-Tool-Using-Python
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate        # Linux/macOS
   venv\Scripts\activate           # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install poppler (required by pdf2image for PDF to Images):**
   - **Ubuntu/Debian:** `sudo apt-get install poppler-utils`
   - **macOS:** `brew install poppler`
   - **Windows:** Download from [poppler releases](https://github.com/oschwartz10612/poppler-windows/releases) and add to PATH.

## Usage

Run the web application:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`. Use the sidebar to select a tool:

1. **PDF to Images** – Upload a PDF, click "Convert to Images", preview pages, and download a ZIP.
2. **Images to PDF** – Upload images, set an output name, click "Convert to PDF", and download.
3. **Merge PDFs** – Upload multiple PDFs, set an output name, click "Merge PDFs", and download.
