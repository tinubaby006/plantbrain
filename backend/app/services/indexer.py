import os

from app.services.parsers.parser import extract_text
from app.services.chunker import chunk_text
from app.services.embeddings import embed_text
from app.services.vector_store import add_chunk


def index_document(file_path: str) -> dict:
    """
    Complete indexing pipeline.

    File
        ↓
    Parse
        ↓
    Chunk
        ↓
    Embed
        ↓
    Store in ChromaDB
    """

    # Extract text
    document = extract_text(file_path)

    text = document["text"]

    # Split into chunks
    chunks = chunk_text(text)

    # Document name
    document_name = os.path.basename(file_path)

    # Store each chunk
  # Store each chunk
    for chunk in chunks:

        embedding = embed_text(chunk["text"])

        chunk_id = f"{document_name}_chunk_{chunk['chunk_id']}"

        metadata = {
            "document": document_name,
            "chunk": int(chunk["chunk_id"]),
            "start": int(chunk["start"]),
            "end": int(chunk["end"]),
        }

        pages = document.get("pages")
        if pages is not None:
            metadata["page_count"] = int(pages)

        add_chunk(
            chunk_id=chunk_id,
            text=chunk["text"],
            embedding=embedding,
            metadata=metadata,
        )
    return {
    "filename": document_name,
    "pages": document.get("pages"),
    "words": document.get("words"),
    "chunks": len(chunks),
    "metadata": document.get("metadata", {}),
}