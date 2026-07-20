from typing import List, Dict


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200,
) -> List[Dict]:
    """
    Split text into overlapping chunks while preserving
    sentence and paragraph boundaries whenever possible.

    Strategy:
    - Target chunk_size characters.
    - Prefer ending at:
        1. Paragraph break (\n\n)
        2. Newline (\n)
        3. Sentence (. ! ?)
        4. Space
    - Maintain overlap between chunks.
    """

    if not text.strip():
        return []

    text = text.strip()
    chunks = []

    start = 0
    chunk_id = 1
    text_length = len(text)

    while start < text_length:

        # Last chunk
        if start + chunk_size >= text_length:
            end = text_length

        else:
            target = start + chunk_size

            candidates = [
                text.rfind("\n\n", start, target),
                text.rfind("\n", start, target),
                text.rfind(". ", start, target),
                text.rfind("! ", start, target),
                text.rfind("? ", start, target),
                text.rfind(" ", start, target),
            ]

            end = max(candidates)

            # If nothing suitable found, use target size
            if end <= start:
                end = target

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "text": chunk,
                    "start": start,
                    "end": end,
                }
            )

            chunk_id += 1

        # Next chunk with overlap
        start = max(end - overlap, start + 1)

    return chunks