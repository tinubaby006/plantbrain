from app.services.embeddings import embed_text
from app.services.vector_store import search


def retrieve(
    query: str,
    top_k: int = 5,
) -> list[dict]:
    """
    Retrieve the most relevant chunks for a user query.

    Pipeline:
        Query
          ↓
        Gemini Embedding
          ↓
        ChromaDB Similarity Search
          ↓
        Top-k Chunks
    """

    # Convert question to embedding
    query_embedding = embed_text(query)

    # Search ChromaDB
    results = search(
        query_embedding=query_embedding,
        top_k=top_k,
    )

    retrieved = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances,
    ):
        retrieved.append(
            {
                "document": metadata.get("document"),
                "chunk": metadata.get("chunk"),
                "start": metadata.get("start"),
                "end": metadata.get("end"),
                "text": document,
                "distance": round(distance, 4),
            }
    )
    return retrieved