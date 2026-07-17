from typing import List, Dict


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200
) -> List[Dict]:
    """
    Split text into overlapping chunks.
    """

    chunks = []

    start = 0
    chunk_id = 1

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]

        chunks.append({
            "chunk_id": chunk_id,
            "text": chunk,
            "start": start,
            "end": min(end, len(text))
        })

        chunk_id += 1

        start += chunk_size - overlap

    return chunks