# PDF-Utility-Tool-Using-Python

This project is a PDF Utility Tool developed using Python with a Tkinter-based interface. It helps users quickly manage documents with a polished desktop UI.

## Features

- Convert PDF files into JPG images
- Convert images into a single PDF file
- Merge multiple PDFs into one
- Split a PDF into individual pages
- Rotate PDF pages by 90/180/270 degrees
- Extract text from a PDF into a `.txt` file

## Prerequisites

### Python

- Python 3.7 or later
- Required packages:
  - `pdf2image`
  - `Pillow`
  - `PyPDF2`

Install the Python dependencies (ideally in a virtual environment) with:

```bash
pip install pdf2image Pillow PyPDF2
```

### Poppler (for `pdf2image`)

The `pdf2image` library requires the Poppler utilities to be installed on your system:

- **Windows**: Download Poppler for Windows from the official builds (e.g. `https://github.com/oschwartz10612/poppler-windows`) and add the `bin` folder to your `PATH`.
- **macOS**: Install via Homebrew:
  ```bash
  brew install poppler
  ```
- **Linux (Debian/Ubuntu-based)**:
  ```bash
  sudo apt-get update
  sudo apt-get install poppler-utils
  ```
- **Linux (Fedora/RHEL-based)**:
  ```bash
  sudo dnf install poppler-utils
  ```

Ensure Poppler is installed and available on your `PATH` before running the application.

## How to Run

After installing the prerequisites, run:

```bash
python3 project.py
```

The GUI will open and guide you through each document action.
