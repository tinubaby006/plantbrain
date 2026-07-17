import easyocr
import cv2
import logging

logger = logging.getLogger(__name__)

_reader = None


def get_reader():
    global _reader

    if _reader is None:
        logger.info("Loading EasyOCR model...")
        _reader = easyocr.Reader(["en"], gpu=False)

    return _reader


def extract_image(file_path: str) -> dict:
    try:
        image = cv2.imread(file_path)

        if image is None:
            raise ValueError("Unable to read image.")

        reader = get_reader()

        results = reader.readtext(image, detail=0)

        text = "\n".join(results)

        return {
            "pages": 1,
            "words": len(text.split()),
            "text": text,
            "metadata": {}
        }

    except Exception as e:
        logger.exception("Image parsing failed")
        raise ValueError(f"Failed to parse image: {e}")