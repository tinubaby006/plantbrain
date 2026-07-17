import pandas as pd
import logging

logger = logging.getLogger(__name__)

def extract_csv(file_path: str) -> dict:
    """
    Extract text from a CSV file.
    
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
        df = pd.read_csv(file_path)
        text = df.to_string(index=False)
        return {
            "pages": None,
            "words": len(text.split()),
            "text": text,
            "metadata": {
                "rows": len(df)
            }
        }
    except Exception as e:
        logger.error(f"Failed to parse CSV {file_path}: {e}")
        raise ValueError(f"Error parsing CSV: {str(e)}") from e