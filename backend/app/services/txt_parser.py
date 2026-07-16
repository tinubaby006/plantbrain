def extract_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    return {
        "pages": 1,
        "words": len(text.split()),
        "text": text
    }