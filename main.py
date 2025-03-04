import sys
import os
import datetime
import requests
import io
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PyPDF2 import PdfReader

def get_pdf_links_from_website(url):    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]
        pdf_links = [urljoin(url, link) for link in pdf_links]
        return pdf_links
    except Exception as e:      
        print('Error: ', e)
        return []
    
def extract_text_from_pdf_link(url):
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
        print('Error: ', e)
        return ""
    
def extract_text_from_local_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    except Exception as e:
        print('Error: ', e)
        return ""

def get_unique_filename(base_filename):
    if not os.path.exists(base_filename):
        return base_filename
    name, ext = os.path.splitext(base_filename)
    counter = 1
    while True:
        new_filename = f"{name}_{counter}{ext}"
        if not os.path.exists(new_filename):
            return new_filename
        counter += 1

def get_pdf_title_from_pdf_link(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        reader = PdfReader(io.BytesIO(response.content))
        title = reader.metadata.get("/Title")
        if title:
            title = "".join(c for c in title if c.isalnum() or c in " _-").strip()
        return title
    except Exception as e:
        print(f"Error extracting PDF title from link {url}:", e)
        return ""

def get_pdf_title_from_local_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        title = reader.metadata.get("/Title")
        if title:
            title = "".join(c for c in title if c.isalnum() or c in " _-").strip()
        return title
    except Exception as e:
        print(f"Error extracting PDF title from local file {file_path}:", e)
        return ""
    
def get_output_filename(source):
    timestamp = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
    
    if source.startswith("http") and source.lower().endswith("pdf"):
        title = get_pdf_title_from_pdf_link(source)
        if title:
            filename = f"{title}_{timestamp}.txt"
            return get_unique_filename(filename)
    elif not source.startswith("http"):
        title = get_pdf_title_from_local_pdf(source)
        if title:
            filename = f"{title}_{timestamp}.txt"
            return get_unique_filename(filename)
    filename = f"output_{timestamp}.txt"
    return get_unique_filename(filename)

def check_source(source):
    extracted_text = ""
    if(source.startswith("http")): # URL
        if(source.endswith("pdf")):
            extracted_text += extract_text_from_pdf_link(source)
        else:
            pdf_links = get_pdf_links_from_website(source)
            print(pdf_links)
            if pdf_links:
                for link in pdf_links:
                    extracted_text += extract_text_from_pdf_link(link)
                    extracted_text += "\n"
            else:
                print("No PDF links found")
    else: # Local file
        extracted_text += extract_text_from_local_pdf(source)
    return extracted_text

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <source>")
        sys.exit(1)
    source = sys.argv[1]
    extracted_text = check_source(source)
    if not extracted_text:
        print("No text extracted from PDFs")
        sys.exit(1)
    output_file = get_output_filename(source)
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(extracted_text)
        print("Text extracted from PDFs successfully saved to", output_file)
    except Exception as e:
        print("Error writing to file:", e)

if __name__ == "__main__":
    main()