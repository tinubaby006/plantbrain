import fitz
import logging

logger = logging.getLogger(__name__)

def extract_pdf(file_path: str) -> dict:
    """
    Extract text from a PDF file.
    
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
        pdf = fitz.open(file_path)
        text = ""
        for page in pdf:
            text += page.get_text()
        
        return {
            "pages": len(pdf),
            "words": len(text.split()),
            "text": text,
            "metadata": {}
        }
    except Exception as e:
        logger.error(f"Failed to parse PDF {file_path}: {e}")
        raise ValueError(f"Error parsing PDF: {str(e)}") from e