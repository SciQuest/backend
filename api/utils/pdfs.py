import fitz


def extract_data(pdf_path: str) -> dict[str, str | list[str]]:
    pdf_text = ""
    with fitz.open(pdf_path) as pdf_file:
        pdf_text = "[PAGE DELIMITER]\n".join([page.get_text() for page in pdf_file])
        pdf_text = "".join(char for char in pdf_text if ord(char) < 128)

    data = {
        "title": "",
        "abstract": "",
        "authors": ["", ""],
        "institutions": ["", "", ""],
        "keywords": ["", ""],
        "text": "",
        "references": [""],
    }

    return data
