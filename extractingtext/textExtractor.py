import requests
import io
from PyPDF2 import PdfReader

class text_extractor:
    @staticmethod
    def extract_text(url, source_type):
        try:
            if(source_type == "online_pdf" or source_type == "website"):
                response = requests.get(url)
                response.raise_for_status()
                reader = PdfReader(io.BytesIO(response.content))
            elif(source_type == "local_pdf"):
                reader = PdfReader(url)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            return text
        except Exception as e:
            print(f"Error extracting text from PDF link {url}:", e)
            return ""
