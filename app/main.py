from fastapi import FastAPI, status, HTTPException, UploadFile, File
from app import schemas
from app.rag.ingestion import ingest_document, run_ingestion
from app.rag.embeddings import chroma_client, MyEmbeddingFunction
from app.rag.parser import parse_uploaded_document
from app.rag.augmenter import build_context, build_prompt
from app.rag.generator import generate_answer

app = FastAPI()

@app.on_event("startup")
def startup_event():
    global collection

    collection = chroma_client.get_or_create_collection(
        "policy_chunks",
        embedding_function=MyEmbeddingFunction()
    )

    if collection.count() == 0:
        run_ingestion()
        collection = chroma_client.get_or_create_collection(
            "policy_chunks",
            embedding_function=MyEmbeddingFunction()
        )

@app.get("/")
def root():
    return {"ok": True}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF files are allowed")
    
    pdf_bytes = await file.read()
    try:
        source, full_text = parse_uploaded_document(pdf_bytes, file.filename)
        ingest_document(source, full_text, collection)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Upload failed: {str(e)}")
    
    return {"message": f"{source} uploaded successfully"}

@app.post("/ask", status_code=status.HTTP_200_OK, response_model=schemas.QuestionResponse)
def ask_query(query: schemas.QuestionCreate):
    
    results = collection.query(
        query_texts=[query.query],
        n_results=5,
        include=["documents", "metadatas"]
    )
    
    if not results["documents"][0]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No relevant academic context found."
)
        
    context = build_context(results)
    prompt = build_prompt(query.query, context)
    try:
        answer = generate_answer(prompt)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    
    sources = set()
    for metadata in results["metadatas"][0]:
        sources.add(metadata["source"])
        
    return {
    "query": query.query,
    "answer": answer,
    "sources": list(sources)
    }
