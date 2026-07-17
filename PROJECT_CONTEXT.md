# PlantBrain AI

## Project Overview

PlantBrain AI is an AI-powered industrial document intelligence platform.

The goal is to allow engineers to upload industrial documents, search them semantically, chat with them using RAG, build a knowledge graph, and eventually support maintenance and compliance intelligence.

Current phase: Hackathon MVP

---

# Tech Stack

## Frontend

- Next.js
- Tailwind CSS
- TypeScript

## Backend

- FastAPI
- Python 3.12+

## AI

- Google Gemini
- LangChain
- ChromaDB

## Knowledge Graph

- Neo4j (later)

---

# Current Roadmap

## ✅ Checkpoint 1

Document Intelligence

Features

- Upload documents
- Extract text
- Parse multiple document types

Supported formats

- PDF
- DOCX
- TXT
- CSV
- XLSX
- XLS
- Images (OCR)

Current parser modules

```
app/services/

pdf_parser.py
docx_parser.py
txt_parser.py
csv_parser.py
excel_parser.py
image_parser.py
parser.py
```

---

## Planned Checkpoint 2

Industrial Search

Workflow

```
Upload

↓

Extract Text

↓

Chunk Text

↓

Generate Embeddings

↓

Store in ChromaDB

↓

Semantic Search
```

---

## Planned Checkpoint 3

Industrial RAG

Workflow

```
User Question

↓

Retriever

↓

Relevant Chunks

↓

Gemini

↓

Answer with Sources
```

---

## Planned Checkpoint 4

Knowledge Graph

Using

- Neo4j
- Cypher

---

## Planned Checkpoint 5

Maintenance AI Agent

Using

- LangGraph
- Gemini
- ChromaDB
- Neo4j

---

# Backend Architecture

```
backend/

app/

main.py

database.py

schemas.py

routers/

uploads.py

services/

parser.py

pdf_parser.py

docx_parser.py

txt_parser.py

csv_parser.py

excel_parser.py

image_parser.py

utils/
```

---

# Parsing Standard

Every parser MUST return exactly this format.

```python
{
    "pages": int | None,
    "words": int,
    "text": str
}
```

All parsers should use:

- type hints
- exception handling
- clean code
- descriptive function names

---

# Coding Style

Requirements

- Pythonic code
- Follow PEP8
- Small reusable functions
- No duplicated code
- Add docstrings
- Add type hints
- Handle errors gracefully
- Keep functions under ~50 lines where practical

---

# API Conventions

Responses should be JSON.

Example

```json
{
    "status": "success",
    "message": "...",
    "data": {}
}
```

---

# Current Goal

Complete Checkpoint 1.

Tasks remaining

- Finish all parsers
- Build parser dispatcher
- Improve upload endpoint
- Store metadata
- Unit test parsers

Do NOT implement embeddings or RAG unless requested.

---

# Future Pipeline

```
Upload

↓

Parser

↓

Chunker

↓

Embeddings

↓

ChromaDB

↓

Retriever

↓

Gemini

↓

Knowledge Graph

↓

Agent
```

---
