from discus import Knowledge
import os
import pytesseract

from PIL import Image
from pdf2image import convert_from_path


k = Knowledge(config = "/Users/NiravShah/Downloads/discus/examples/eng2spanish/eng2spanish.json")
raw_data = k.extract_data("/Users/NiravShah/Downloads/discus/knowledgeTesting/data")
print(len(raw_data))
for v1, v2 in raw_data.values():
    print(f"{v1}\n")
    print(f"f{v2} \n \n ")

for k in raw_data.keys():
    print(f"{k} \n\n")

def extract_data(path):
        """TODO: add docstring"""
        """TODO: extract metadata"""
        #supports txts and pdfs 
        
        raw_data = {}

        for file_name in os.listdir(path):
            file_path = os.path.join(path, file_name)
            file_extension = os.path.splitext(file_path)[1].lower()
            content = ""
            metadata = {}

            try:
                if file_extension == ".txt":
                    with open(file_path, "r") as file:
                        content = file.read()
                elif file_extension == ".pdf":
                    images = convert_from_path(file_path)
                    for image in images:
                        text = pytesseract.image_to_string(image)
                        content += text
                else:
                    raise IOError
                
                if content:
                    raw_data[file_path] = (metadata, content)

            except IOError as e:
                print(f"{file_path} is unreadable (hint: make sure your knowledge base directory only contains files of type .txt or .pdf")


        return raw_data


# raw_data = extract_data("/Users/NiravShah/Downloads/discus/knowledgeTesting/data")
# print(len(raw_data))
# print(raw_data)

