import threading
import openai
import fitz
import datetime
import os
import re
import json


def extract_data(pdf_path: str) -> dict[str, str | list[str]]:
    with fitz.open(pdf_path) as pdf_file:
        pdf_text = "\n".join([page.get_text() for page in pdf_file])
        pdf_text = "".join(char for char in pdf_text if ord(char) < 128)

        first_page_text = pdf_file[0].get_text()
        first_page_text = "".join(char for char in first_page_text if ord(char) < 128)

    match = re.compile(r"(?is).*references(.*)").search(pdf_text)
    references_text = match.group(1) if match else ""

    lock = threading.Lock()
    data = {
        "title": None,
        "abstract": None,
        "authors": None,
        "institutions": None,
        "keywords": None,
        "text": pdf_text,
        "references": None,
        "date": None,
    }

    def openai_request1():
        openai_client1 = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        completion1 = openai_client1.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in analyzing scientific research papers."
                    + "From the following text extract informations without making any modification. put them in the following json format that contains only the following elements :"
                    + " title"
                    + " abstract"
                    + " authors"
                    + " institutions"
                    + " keywords"
                    + " publication_date"
                    + "\n for the authors and institutions ,add only their names . "
                    + "\n for the publication date use iso format (yyyy-mm-dd) "
                    + "\n for the abstract extract all its content "
                    + "\n",
                },
                {"role": "user", "content": first_page_text},
            ],
        )

        response1 = json.loads(completion1.choices[0].message.content)

        lock.acquire()
        data["title"] = response1["title"]
        data["abstract"] = response1["abstract"]
        data["authors"] = response1["authors"]
        data["institutions"] = response1["institutions"]
        data["keywords"] = response1["keywords"]
        data["date"] = (datetime.date.fromisoformat(response1["publication_date"]),)
        lock.release()

    def openai_request2():
        openai_client2 = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        completion2 = openai_client2.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in analyzing scientific research papers."
                    + "From the following text extract informations without making any modification. put them in the following json format that contains only the references in a list of strings :"
                    + " references"
                    + "\n",
                },
                {"role": "user", "content": references_text},
            ],
        )

        response2 = json.loads(completion2.choices[0].message.content)

        lock.acquire()
        data["references"] = response2["references"]
        lock.release()

    thread1 = threading.Thread(target=openai_request1)
    thread2 = threading.Thread(target=openai_request2)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    return data
