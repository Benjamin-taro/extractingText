import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class urlFinder:
    def get_pdf_links_from_website(url):
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