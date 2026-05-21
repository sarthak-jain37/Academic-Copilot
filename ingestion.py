from chunker import chunk_document
from parser import parse_document
from embeddings import chroma_client, MyEmbeddingFunction

documents = [
    "docs/Deans List Criteria.pdf",
    "docs/Examination Manual.pdf",
    "docs/Minor Programme at SNU.pdf",
    "docs/Policy on Academic Standards.pdf",
    "docs/Policy on Attendance Requirements for Undergraduate Students.pdf",
    "docs/Policy on Common Core Curriculum.pdf",
    "docs/Policy on Credit Limit and Credit Extension.pdf",
    "docs/Policy on Grading System.pdf",
    "docs/Policy on Minimum Class Size.pdf",
]    
 
def ingest_document(source, full_text, collection):
    if full_text is None:
        return

    doc_chunks = chunk_document(full_text, chunk_size=750, overlap=100)

    all_ids = []
    all_metadata = []

    for i in range(len(doc_chunks)):
        all_ids.append(f"{source}_chunk_{i}")
        all_metadata.append({"source": source})

    collection.delete(where={"source": source})

    collection.add(
        documents=doc_chunks,
        ids=all_ids,
        metadatas=all_metadata
    )   

def run_ingestion():
    try:
        chroma_client.delete_collection("policy_chunks")
    except Exception:
        pass

    collection = chroma_client.get_or_create_collection(
        "policy_chunks",
        embedding_function=MyEmbeddingFunction()
    )

    for document in documents:
        source, full_text = parse_document(document)
        ingest_document(source, full_text, collection)
