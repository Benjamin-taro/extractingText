import sys
import os
import datetime
import requests
import io
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PyPDF2 import PdfReader

class PDFExtractor:
    def __init__(self, source):
        """
        source: PDF URL, local file path, or a website URL containing PDF links.
        """
        self.source = source

    def get_pdf_links_from_website(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            # Find all links that end with .pdf
            pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].lower().endswith('.pdf')]
            # Convert relative URLs to absolute URLs
            pdf_links = [urljoin(url, link) for link in pdf_links]
            return pdf_links
        except Exception as e:
            print("Error retrieving PDF links from website:", e)
            return []

    def extract_text_from_pdf_link(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            reader = PdfReader(io.BytesIO(response.content))
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            return text
        except Exception as e:
            print(f"Error extracting text from PDF link {url}:", e)
            return ""

    def extract_text_from_local_pdf(self, file_path):
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            return text
        except Exception as e:
            print(f"Error extracting text from local PDF {file_path}:", e)
            return ""

    def get_pdf_title_from_pdf_link(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            reader = PdfReader(io.BytesIO(response.content))
            title = reader.metadata.get("/Title")
            if title:
                # Remove characters that are not allowed in filenames
                title = "".join(c for c in title if c.isalnum() or c in " _-").strip()
            return title
        except Exception as e:
            print(f"Error extracting PDF title from link {url}:", e)
            return ""

    def get_pdf_title_from_local_pdf(self, file_path):
        try:
            reader = PdfReader(file_path)
            title = reader.metadata.get("/Title")
            if title:
                title = "".join(c for c in title if c.isalnum() or c in " _-").strip()
            return title
        except Exception as e:
            print(f"Error extracting PDF title from local file {file_path}:", e)
            return ""

    @staticmethod
    def get_unique_filename(base_filename):
        """
        If base_filename already exists, add a counter to create a unique filename.
        """
        if not os.path.exists(base_filename):
            return base_filename
        name, ext = os.path.splitext(base_filename)
        counter = 1
        while True:
            new_filename = f"{name}_{counter}{ext}"
            if not os.path.exists(new_filename):
                return new_filename
            counter += 1

    def get_output_filename(self):

        timestamp = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
        # If the source is a direct PDF URL
        if self.source.startswith("http") and self.source.lower().endswith("pdf"):
            title = self.get_pdf_title_from_pdf_link(self.source)
            if title:
                filename = f"{title}_{timestamp}.txt"
                return self.get_unique_filename(filename)
        # If the source is a local PDF file
        elif not self.source.startswith("http"):
            title = self.get_pdf_title_from_local_pdf(self.source)
            if title:
                filename = f"{title}_{timestamp}.txt"
                return self.get_unique_filename(filename)
        # Otherwise, use a default output filename with a timestamp
        filename = f"output_{timestamp}.txt"
        return self.get_unique_filename(filename)

    def process_source(self):
        extracted_text = ""
        if self.source.startswith("http"):
            if self.source.lower().endswith("pdf"):
                extracted_text += self.extract_text_from_pdf_link(self.source)
            else:
                pdf_links = self.get_pdf_links_from_website(self.source)
                print("Found PDF links:", pdf_links)
                if pdf_links:
                    for link in pdf_links:
                        extracted_text += self.extract_text_from_pdf_link(link)
                        extracted_text += "\n"
                else:
                    print("No PDF links found on the website.")
        else:
            extracted_text += self.extract_text_from_local_pdf(self.source)
        return extracted_text

    def save_output(self, text):
        output_file = self.get_output_filename()
        try:
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(text)
            print("Text extracted from PDFs successfully saved to", output_file)
        except Exception as e:
            print("Error writing to file:", e)


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <source>")
        sys.exit(1)
    source = sys.argv[1]
    extractor = PDFExtractor(source)
    extracted_text = extractor.process_source()
    if not extracted_text:
        print("No text extracted from PDFs")
        sys.exit(1)
    extractor.save_output(extracted_text)

if __name__ == "__main__":
    main()
