import os
import pytesseract

from PIL import Image
from pdf2image import convert_from_path
from discus.json.architecture import schema
from discus.json.config import DiscusConfig


class Knowledge: 
    
    def __init__(self, config):
        """Initializes Knowledge class with config"""
        self.config = DiscusConfig(config)
        self.raw_data = {} #Structure: {"filename": ({metadata}, "content")}
        self.chunked_data = {}
        self.db_path = ""


    def _validate_config(self):
        """Validates the config against supported models and task types."""

        """TODO: Add validation process for embedding models either here or in gneerator class"""
        pass

    def extract_data(self, path):
        """TODO: add docstring"""
        """TODO: extract metadata"""
        #supports pdfs, images, 
        for root, _, files in os.walk(path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                file_extension = os.path.splitext(file_path)[1].lower()
                content = ""
                metadata = {}
                
                try:
                    if file_extension == ".txt":
                        with open(file_path, "r") as file:
                            content = file.read()
                    else:
                        if file_extension == ".pdf":
                            images = convert_from_path(file_path)
                            for image in images:
                                text = pytesseract.image_to_string(image)
                                content += text
                        elif file_extension in [".img", ".jpg", ".jpeg", ".png", ".ico"]: 
                            images = Image.open(file_path)
                            content = pytesseract.image_to_string(image)
                        else:
                            raise IOError
                except IOError as _:
                    print(f"{file_path} is unreadable (hint: make sure your knowledge base directory only contains files of type .txt or .pdf")

                if content != "":
                    self.raw_data[file_path] = (metadata, content)

        return self.raw_data

    def chunk_data():
        pass

    def generate_embeddings():
        pass

    def retrieve():
        pass

