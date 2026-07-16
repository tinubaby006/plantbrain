import fitz 
def extract_pdf(file_path):
    pdf = fitz.open(file_path)

    text = ""

    for page in pdf:
        text += page.get_text()

    return {
        "pages": len(pdf),
        "words": len(text.split()),
        "text": text
    }