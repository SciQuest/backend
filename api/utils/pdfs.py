from datetime import date
from PyPDF2 import PdfReader
import re
import os
from openai import OpenAI
from dotenv import load_dotenv
import json


def extract_references(text):
        pattern = re.compile(r"(?is).*references(.*)")#legendary regular expression LOL it solves 90% of our problems
        match = pattern.search(text)
        if match:
            return match.group(1)
        else:
            return None

def extract_data(pdf_path: str) -> dict[str, str | list[str]]:
    pdf_text = ""
    
    reader = PdfReader(pdf_file)
    pdf_text = ""
    with open(pdf_file, "rb") as pdf_file:
        reader=PdfReader(pdf_file)
        pdf_text = "\n".join([reader.pages[i].extract_text() for i in range(len(reader.pages))])
        pdf_text = "".join(char for char in pdf_text if ord(char) < 128)
        #print(pdf_text)
        
    num_pages = len(reader.pages)
    first_pages = [reader.pages[i] for i in range(num_pages) if (i < 1)] # first page

    text1 = ""
    text2 = ""

    for page in first_pages:
        text1 +=  page.extract_text()
        text1+= "\n"

    # Use regular expression to extract everything after "References" 
    references = extract_references(pdf_text)
    print(references)    

        
    
    data = {
        "title": pdf_path,
        "abstract": "",
        "authors": ["", ""],
        "institutions": ["", "", ""],
        "keywords": ["", ""],
        "text": "",
        "references": [""],
        "date": date.today(),
    }

    return data
