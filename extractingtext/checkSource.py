class check_source:
    def check(source):
        if source.startswith("http") and source.lower().endswith("pdf"): #direct link to pdf
            return "online_pdf"
        elif source.startswith("http"): #website link
            return "website"
        else: #local pdf file
            return "local_pdf"