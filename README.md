# Extracting Text From PDF

This script allow us to extract text from pdf files. It supports three types of sources:

- Online PDF: A direct URL to a PDF file.
- Local PDF: A locaal file path to a PDF.
- Website: A URL to a website which is potentially containing linked to PDF files.

This script will extract text from each PDF and produced txt file for each PDF files and stored in afolder named by the current date.

# Project Structure
extractingtext/
├── extractingtext/            <-- Package folder
│   ├── __init__.py
│   ├── check_source.py
│   ├── url_finder.py
│   ├── text_extractor.py
│   ├── save_output.py
├── main.py
└── README.md

# Usage
Run the script from the command line:
python main.py <source>
where source shoud be one of the following:
- A direct URL to a PDF (e.g., https://example.com/document.pdf).
- A URL to a website that contains PDF links (e.g., https://example.com/articles).
- A local PDF file path (e.g., document.pdf).