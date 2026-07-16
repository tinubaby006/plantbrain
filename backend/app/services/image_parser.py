import easyocr
import cv2

# Load the OCR model once (faster for multiple requests)
reader = easyocr.Reader(['en'], gpu=False)


def extract_image(file_path: str) -> dict:
    """
    Extract text from an image using OCR.

    Returns:
    {
        "pages": 1,
        "words": 123,
        "text": "Extracted text..."
    }
    """

    image = cv2.imread(file_path)

    if image is None:
        raise ValueError("Unable to read image.")

    results = reader.readtext(image, detail=0)

    text = "\n".join(results)

    return {
        "pages": 1,
        "words": len(text.split()),
        "text": text
    }