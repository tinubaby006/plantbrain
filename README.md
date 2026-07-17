# 🌱 PlantBrain

PlantBrain is an AI-powered document intelligence system that enables users to upload documents, extract text, create embeddings, build a vector index, and perform Retrieval-Augmented Generation (RAG) for intelligent question answering.

## 🚀 Features

- 📄 Multi-format document parsing
  - PDF
  - DOCX
  - TXT
  - CSV
  - Excel
  - Images (OCR)

- ✂️ Intelligent document chunking

- 🧠 Embedding generation

- 📚 Vector database indexing

- 🔍 Semantic document retrieval

- 🤖 Retrieval-Augmented Generation (RAG)

- ⚡ FastAPI backend

---

## Project Structure

```
plantbrain/
│
├── backend/
│   ├── app/
│   │   ├── services/
│   │   │   ├── parsers/
│   │   │   ├── chunker.py
│   │   │   ├── embeddings.py
│   │   │   ├── indexer.py
│   │   │   ├── rag.py
│   │   │   ├── retriever.py
│   │   │   └── vector_store.py
│   │   └── main.py
│   ├── requirements.txt
│   └── .gitignore
│
└── README.md
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/tinubaby006/plantbrain.git
cd plantbrain
```

### Create a virtual environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file inside the `backend` directory.

Example:

```env
GEMINI_API_KEY=your_api_key
```

(Add any additional environment variables required by your project.)

---

## Run the Backend

```bash
cd backend
uvicorn app.main:app --reload
```

The API will be available at

```
http://127.0.0.1:8000
```

Swagger documentation

```
http://127.0.0.1:8000/docs
```

---

## Workflow

1. Upload a document
2. Extract document text
3. Split text into chunks
4. Generate embeddings
5. Store embeddings in the vector database
6. Retrieve relevant chunks
7. Generate an AI-powered answer using RAG

---

## Future Improvements

- Conversation memory
- Multi-document search
- User authentication
- Cloud deployment
- Streaming responses
- Hybrid search
- Citation support

---
