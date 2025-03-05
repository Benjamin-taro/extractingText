# Extracting Text From PDF

This script allows us to extract text from pdf files. It supports three types of sources:

- Online PDF: A direct URL to a PDF file.
- Local PDF: A local file path to a PDF.
- Website: A URL to a website which potentially contains links to PDF files.

This script will extract text from each PDF and produce text files for each PDF file and store them in a folder named by the current date.

# Project Structure
```
extractingtext/
├── extractingtext/
│   ├── __init__.py
│   ├── check_source.py
│   ├── url_finder.py
│   ├── text_extractor.py
│   ├── save_output.py
├── main.py
└── README.md
```
# Usage
Run the script from the command line:
``` bash
python main.py <source>
```
where source should be one of the following:
- A direct URL to a PDF (e.g., https://example.com/document.pdf).
- A URL to a website that contains PDF links (e.g., https://example.com/articles).
- A local PDF file path (e.g., document.pdf).
