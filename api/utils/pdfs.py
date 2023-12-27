def extract_data(pdf_path: str) -> dict[str, str | list[str]]:
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
