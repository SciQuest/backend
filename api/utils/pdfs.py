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
    reader = PdfReader(pdf_file)
    pdf_text = ""
    with open(pdf_file, "rb") as pdf_file:
        reader=PdfReader(pdf_file)
        pdf_text = "\n".join([reader.pages[i].extract_text() for i in range(len(reader.pages))])
        pdf_text = "".join(char for char in pdf_text if ord(char) < 128)
        
    num_pages = len(reader.pages)
    first_pages = [reader.pages[i] for i in range(num_pages) if (i < 2)] # first two pages
    text = ""
    for page in first_pages:
        text +=  page.extract_text()
        text+= "\n"

    # Use regular expression to extract everything after "References" 
    references = extract_references(pdf_text)
    
    title_date = {
        "title": pdf_path,
        "date": date.today(),
        "text":pdf_text
    }
    client1 = OpenAI()
    client2 = OpenAI()
    completion1 = client1.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an expert in analyzing scientific research papers."+"From the following text extract informations without making any modification. put them in the following json format that contains only the following elements :"+
                " abstract"+
                " authors"+
                " institutions"+
                " keywords"+"\n for the authors and institutions ,add only their names . "+"\n" },
        {"role": "user", "content": text}
    ]
    )
    #multiprocessing should be between completion1 and completion2
    completion2 = client2.chat.completions.create(
    model="gpt-3.5-turbo-16k",
    messages=[
        {"role": "system", "content": "You are an expert in analyzing scientific research papers."+"From the following text extract informations without making any modification. put them in the following json format that contains only the references in a list of strings :"+
                " {references"+"\n" },
        {"role": "user", "content": references}
    ]
    )

    dict1 = json.loads(completion1.choices[0].message.content)
    dict2 = json.loads(completion2.choices[0].message.content)

    merged_dict = {**dict1, **dict2}
    result = json.dumps(merged_dict, indent=2)
    data= {**result,**title_date}

    return data
