from docx import Document

def extract_docx(file_path):
    doc = Document(file_path)

    text = "\n".join(
        paragraph.text
        for paragraph in doc.paragraphs
        if paragraph.text.strip()
    )

    return {
        "pages": None,
        "words": len(text.split()),
        "text": text
    }