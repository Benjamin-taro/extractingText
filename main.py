import sys
from extractingtext.checkSource import check_source
from extractingtext.urlFinder import urlFinder
from extractingtext.textExtractor import text_extractor
from extractingtext.saveOutput import saveOutput

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <source>")
        sys.exit(1)
    source = sys.argv[1]
    source_type = check_source.check(source)
    urls = []
    if source_type == "website":
        urls = urlFinder.get_pdf_links_from_website(source)
    else:
        urls.append(source)
    if not urls:
        print("No PDF links found in the source")
        sys.exit(1)
    for url in urls:
        extracted_text = ""
        extracted_text += text_extractor.extract_text(url, source_type)
        if not extracted_text:
            print("No text extracted from", url)
            continue
        saveOutput.save(extracted_text, url)


if __name__ == "__main__":
    main()
