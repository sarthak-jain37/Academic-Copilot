from chunker import chunk_document
from parser import parse_document
from embeddings import client, MyEmbeddingFunction

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

chunks = []
all_ids = []
all_metadata = []

try:
    client.delete_collection("policy_chunks")
except:
    pass 

collection = client.get_or_create_collection(
    "policy_chunks",
    embedding_function=MyEmbeddingFunction()
)


for document in documents:
    source, full_text = parse_document(document)
    if full_text is None:
        continue
    
    try:
        doc_chunks = chunk_document(full_text, chunk_size=750, overlap=100)
        chunks.extend(doc_chunks)
        print(f"{source} chunking successful ({len(doc_chunks)} chunks)")

    except Exception as e:
        print(f"{source}: {e}")
        continue
    
    # IDs + metadata
    try:
        for i in range(len(doc_chunks)):
            all_ids.append(f"{source}_chunk_{i}")
            all_metadata.append({"source": source})

        print(f"{source} IDs and metadata created")

    except Exception as e:
        print(f"Failed creating IDs/metadata for {source}: {e}")
        continue

collection.add(
    documents=chunks,
    ids=all_ids,
    metadatas=all_metadata
)

print("\nAll chunks added to Chroma successfully")