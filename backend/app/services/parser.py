
from pathlib import Path

from .pdf_parser import extract_pdf
from .docx_parser import extract_docx
from .txt_parser import extract_txt
from .csv_parser import extract_csv
from .excel_parser import extract_excel
from .image_parser import extract_image


def extract_text(file_path: str):
    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return extract_pdf(file_path)

    elif extension == ".docx":
        return extract_docx(file_path)

    elif extension == ".txt":
        return extract_txt(file_path)

    elif extension == ".csv":
        return extract_csv(file_path)

    elif extension in [".xlsx", ".xls"]:
        return extract_excel(file_path)

    elif extension in [".png", ".jpg", ".jpeg", ".tif", ".tiff"]:
        return extract_image(file_path)

    else:
        raise ValueError(f"Unsupported file type: {extension}")
    
