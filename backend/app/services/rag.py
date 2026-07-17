import os
import logging

from dotenv import load_dotenv
from google import genai

from app.services.retriever import retrieve

load_dotenv()

logger = logging.getLogger(__name__)

_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

_SYSTEM_PROMPT = """You are PlantBrain AI, an expert assistant for industrial document intelligence.

You answer questions strictly based on the provided context excerpts from uploaded documents.

Rules:
- Only use information from the context below.
- If the context does not contain enough information, say so clearly.
- Always cite the source document and chunk number for every claim.
- Be concise, accurate, and professional.
- Do not hallucinate or add external knowledge.
"""


def _build_context_block(chunks: list[dict]) -> str:
    """
    Format retrieved chunks into a numbered context block for the prompt.
    """
    lines = []

    for i, chunk in enumerate(chunks, start=1):
        doc = chunk.get("document", "unknown")
        chunk_num = chunk.get("chunk", "?")
        text = chunk.get("text", "").strip()
        lines.append(f"[{i}] Source: {doc} (chunk {chunk_num})\n{text}")

    return "\n\n".join(lines)


def _build_prompt(question: str, context_block: str) -> str:
    """
    Compose the full prompt sent to Gemini.
    """
    return (
        f"{_SYSTEM_PROMPT}\n\n"
        f"--- CONTEXT ---\n{context_block}\n\n"
        f"--- QUESTION ---\n{question}\n\n"
        f"--- ANSWER ---"
    )


def answer(
    question: str,
    top_k: int = 5,
    model: str = "gemini-2.0-flash",
) -> dict:
    """
    Full RAG pipeline: retrieve relevant chunks → generate a grounded answer.

    Pipeline:
        User Question
          ↓
        Retriever (ChromaDB similarity search)
          ↓
        Relevant Chunks
          ↓
        Gemini (grounded generation)
          ↓
        Answer with Sources

    Args:
        question: The user's natural-language question.
        top_k:    Number of chunks to retrieve from the vector store.
        model:    Gemini model identifier to use for generation.

    Returns:
        dict with keys:
            - answer (str): Gemini's grounded response.
            - sources (list[dict]): The retrieved chunks used as context.
            - question (str): The original question (echoed back).
    """
    logger.info(f"RAG query: {question!r}  top_k={top_k}")

    # Step 1 — Retrieve relevant chunks
    chunks = retrieve(question, top_k=top_k)

    if not chunks:
        logger.warning("No chunks retrieved; returning empty-context response.")
        return {
            "question": question,
            "answer": (
                "I could not find any relevant information in the uploaded documents "
                "to answer your question."
            ),
            "sources": [],
        }

    # Step 2 — Build prompt
    context_block = _build_context_block(chunks)
    prompt = _build_prompt(question, context_block)

    # Step 3 — Generate answer with Gemini
    response = _client.models.generate_content(
        model=model,
        contents=prompt,
    )

    answer_text = response.text.strip()

    logger.info(f"RAG answer generated ({len(answer_text)} chars, {len(chunks)} sources).")

    return {
        "question": question,
        "answer": answer_text,
        "sources": chunks,
    }
