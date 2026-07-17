from docx import Document
import logging

logger = logging.getLogger(__name__)

def extract_docx(file_path: str) -> dict:
    """
    Extract text from a DOCX file.
    
    Returns:
        dict: Standardized layout:
            {
                "pages": int | None,
                "words": int,
                "text": str,
                "metadata": dict
            }
    """
    try:
        doc = Document(file_path)
        text = "\n".join(
            paragraph.text
            for paragraph in doc.paragraphs
            if paragraph.text.strip()
        )
        return {
            "pages": None,
            "words": len(text.split()),
            "text": text,
            "metadata": {}
        }
    except Exception as e:
        logger.error(f"Failed to parse DOCX {file_path}: {e}")
        raise ValueError(f"Error parsing DOCX: {str(e)}") from e