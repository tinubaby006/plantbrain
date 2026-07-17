import pandas as pd
import logging

logger = logging.getLogger(__name__)

def extract_excel(file_path: str) -> dict:
    """
    Extract text from an Excel file.
    
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
        sheets = pd.read_excel(file_path, sheet_name=None)
        text = ""
        for name, sheet in sheets.items():
            text += f"\nSheet: {name}\n"
            text += sheet.to_string(index=False)
            
        return {
            "pages": None,
            "words": len(text.split()),
            "text": text,
            "metadata": {
                "sheets": len(sheets)
            }
        }
    except Exception as e:
        logger.error(f"Failed to parse Excel {file_path}: {e}")
        raise ValueError(f"Error parsing Excel: {str(e)}") from e