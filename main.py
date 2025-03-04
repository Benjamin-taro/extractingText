import sys
from checkSource import check_source
from urlFinder import urlFinder
from textExtractor import text_extractor
from saveOutput import saveOutput

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <source>")
        sys.exit(1)
    source = sys.argv[1]
    source_type = check_source.check(source)
    print("Source type:", source_type)
    urls = []
    if source_type == "website":
        urls = urlFinder.get_pdf_links_from_website(source)
    else:
        urls.append(source)
    for url in urls:
        extracted_text = ""
        extracted_text += text_extractor.extract_text(url, source_type)
        if not extracted_text:
            print("No text extracted from", url)
            continue
        saveOutput.save(extracted_text)


if __name__ == "__main__":
    main()
