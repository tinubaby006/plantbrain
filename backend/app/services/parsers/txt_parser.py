import logging

logger = logging.getLogger(__name__)

def extract_txt(file_path: str) -> dict:
    """
    Extract text from a TXT file.
    
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
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        return {
            "pages": 1,
            "words": len(text.split()),
            "text": text,
            "metadata": {}
        }
    except Exception as e:
        logger.error(f"Failed to parse TXT {file_path}: {e}")
        raise ValueError(f"Error parsing TXT: {str(e)}") from e