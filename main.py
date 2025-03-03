import sys
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
        return None
    
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
        return None
    
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
        return None

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
    output_file = "output.txt"
    try:
        with open(output_file, "w") as file:
            file.write(extracted_text)
        print("Text extracted from PDFs successfully saved to", output_file)
    except Exception as e:
        print('Error: ', e)

if __name__ == "__main__":
    main()