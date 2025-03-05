# Extracting Text From PDF

This script allows us to extract text from pdf files. It supports three types of sources:

- Online PDF: A direct URL to a PDF file.
- Local PDF: A local file path to a PDF.
- Website: A URL to a website, which potentially contains links to PDF files.

This script extracts text from each PDF and generates corresponding text files for each PDF.
Then, it saves text files named with f"{pdf_name}_{timestamp}.txt" and stores them into a date-named folder.

# Project Structure
```
extractingtext/
├── extractingtext/ <- Package folder containing the core modules
│   ├── __init__.py <- Initialized the extractingtext package
│   ├── check_source.py <- Determines the type of source
│   ├── url_finder.py <- Extracts PDF links from a website.
│   ├── text_extractor.py <- Extracts text from PDF files
│   ├── save_output.py <- Saves the extracted text into files inside a date-named folder
├── main.py <- Main script that orchestrates the extraction process
└── README.md <- project documentation
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

# Acknowledgements
This project leverages several open sources libraries:
- PyPDF2: For reading and extracting text from PDF files.
- Requests: For handling HTTP requests.
- BeautifulSoup4: For parsing HTML and extracting PDF links from websites.

Special thanks to all the contributors of these open source projects for making this work possible.