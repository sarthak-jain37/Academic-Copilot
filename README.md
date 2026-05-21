# Academic Copilot

RAG-powered academic policy assistant built with FastAPI, ChromaDB, Sentence Transformers, and Gemini.


## Features

- Ask academic policy questions
- Upload new PDF policy documents
- Semantic retrieval with ChromaDB
- Source attribution
- Automatic startup ingestion


## Tech Stack

- FastAPI
- ChromaDB
- Sentence Transformers
- Gemini API
- PyMuPDF


## Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
HF_TOKEN=your_huggingface_token
```


### Notes

- `GEMINI_API_KEY` is required for answer generation.
- `HF_TOKEN` is optional but recommended to avoid Hugging Face rate-limit warnings when downloading embedding models.


## Run the Application

```bash
uv sync
uv run uvicorn app.main:app --reload
```
