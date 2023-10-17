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

