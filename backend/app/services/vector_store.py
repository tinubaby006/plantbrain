import chromadb

# Create (or load) a local Chroma database
client = chromadb.PersistentClient(path="chroma_db")

# Create (or get) the collection
collection = client.get_or_create_collection(
    name="plantbrain_documents"
)


def add_chunk(
    chunk_id: str,
    text: str,
    embedding: list[float],
    metadata: dict | None = None,
):
    """
    Store one chunk and its embedding.
    """

    clean_metadata = {
        k: v
        for k, v in (metadata or {}).items()
        if v is not None
    }

    collection.add(
        ids=[chunk_id],
        documents=[text],
        embeddings=[embedding],
        metadatas=[clean_metadata],
    )


def search(
    query_embedding: list[float],
    top_k: int = 5,
):
    """
    Find the most similar chunks.
    """

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    return results


def count():
    """
    Number of stored chunks.
    """
    return collection.count()