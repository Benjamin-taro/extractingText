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
    def save(text):
        folder = saveOutput.get_output_folder()
        timestamp = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
        filename = f"output_{timestamp}.txt"
        filepath = os.path.join(folder, filename)
        try:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(text)
            print("Text extracted from PDFs successfully saved to", filepath)
            time.sleep(1)

        except Exception as e:
            print("Error writing to file:", e)