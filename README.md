# Academic Copilot

RAG-powered academic policy assistant built with FastAPI, ChromaDB, Sentence Transformers, and Gemini.

Features:
- Ask academic policy questions
- Upload new PDF policy documents
- Semantic retrieval with ChromaDB
- Source attribution
- Automatic startup ingestion

Tech Stack:
- FastAPI
- ChromaDB
- Sentence Transformers
- Gemini API
- PyMuPDF

Run:
uv sync
uv run uvicorn app.main:app --reload