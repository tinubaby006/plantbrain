from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging

from app.routers.uploads import save_upload
from app.services.indexer import index_document
from app.services.retriever import retrieve
from app.services.gemini import answer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PlantBrain AI Backend",
    version="1.0.0"
)


# ---------------------------------------------------------------------------
# Request bodies
# ---------------------------------------------------------------------------

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5
    model: str = "gemini-2.0-flash"


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "PlantBrain AI Backend is running",
        "data": {}
    }


# ---------------------------------------------------------------------------
# Upload & Index
# ---------------------------------------------------------------------------

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document and index it into the vector database.

    Pipeline: Save → Parse → Chunk → Embed → Store in ChromaDB
    """
    try:
        logger.info(f"Uploading file: {file.filename}")

        file_path = save_upload(file)
        result = index_document(file_path)

        return {
            "status": "success",
            "message": "Document indexed successfully",
            "data": result
        }

    except ValueError as e:
        logger.warning(str(e))
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": str(e), "data": {}}
        )

    except Exception as e:
        logger.exception("Unexpected server error during upload")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "Internal server error", "data": {}}
        )


# ---------------------------------------------------------------------------
# Semantic Search
# ---------------------------------------------------------------------------

@app.post("/search")
def search_documents(body: SearchRequest):
    """
    Semantic similarity search across all indexed documents.

    Returns the top-k most relevant chunks with source metadata.
    Does NOT generate an answer — raw retrieval only.
    """
    try:
        logger.info(f"Search query: {body.query!r}  top_k={body.top_k}")

        chunks = retrieve(body.query, top_k=body.top_k)

        return {
            "status": "success",
            "message": f"{len(chunks)} result(s) found",
            "data": {
                "query": body.query,
                "results": chunks
            }
        }

    except Exception as e:
        logger.exception("Search failed")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "Search failed", "data": {}}
        )


# ---------------------------------------------------------------------------
# RAG — Ask a question, get a grounded answer
# ---------------------------------------------------------------------------

@app.post("/query")
def query_documents(body: QueryRequest):
    """
    RAG endpoint: retrieve relevant chunks → generate a grounded answer via Gemini.

    Pipeline: Question → Retriever → Context → Gemini → Answer + Sources
    """
    try:
        logger.info(f"RAG query: {body.question!r}  top_k={body.top_k}")

        result = answer(
            question=body.question,
            top_k=body.top_k,
            model=body.model,
        )

        return {
            "status": "success",
            "message": "Answer generated",
            "data": result
        }

    except Exception as e:
        logger.exception("RAG query failed")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "Query failed", "data": {}}
        )