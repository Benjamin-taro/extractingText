import os
import datetime
import time

class saveOutput:
    @staticmethod
    def get_output_folder():
        folder_name = datetime.datetime.now().strftime("%Y%m%d")
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        return folder_name
    
    @staticmethod
    def get_pdf_name(url):
        pdf_name = url.split("/")[-1][:-4]
        return pdf_name

    @staticmethod 
    def save(text, url):
        folder = saveOutput.get_output_folder()
        timestamp = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
        pdf_name = saveOutput.get_pdf_name(url)
        filename = f"{pdf_name}_{timestamp}.txt"
        filepath = os.path.join(folder, filename)
        try:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(text)
            print("Text extracted from PDFs successfully saved to", filepath)
            time.sleep(1)

        except Exception as e:
            print("Error writing to file:", e)