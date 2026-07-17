from pathlib import Path
import logging

from .pdf_parser import extract_pdf
from .docx_parser import extract_docx
from .txt_parser import extract_txt
from .csv_parser import extract_csv
from .excel_parser import extract_excel
from .image_parser import extract_image

logger = logging.getLogger(__name__)

def extract_text(file_path: str) -> dict:
    """
    Dispatcher function to extract text from a file based on its extension.

    Returns:
        dict: Standardized layout:
            {
                "pages": int | None,
                "words": int,
                "text": str,
                "metadata": dict
            }
    """
    extension = Path(file_path).suffix.lower()
    logger.info(f"Extracting text from: {file_path} (detected type: {extension})")

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
        logger.error(f"Unsupported file type requested: {extension}")
        raise ValueError(f"Unsupported file type: {extension}")
