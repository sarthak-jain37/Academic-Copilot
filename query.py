from embeddings import client, MyEmbeddingFunction
from augmenter import build_context, build_prompt
from generator import generate_answer

collection = client.get_or_create_collection(
    "policy_chunks",
    embedding_function=MyEmbeddingFunction()
)

while True:
    query = input("Ask a question (type exit to quit): ")

    if query.lower() == "exit":
        break

    results = collection.query(
        query_texts=[query],
        n_results=5,
        include=["documents", "metadatas"]
    )
    
    if not results["documents"][0]:
        print("No relevant context found.")
        exit()
    
    context = build_context(results)
    prompt = build_prompt(query, context)
    
    answer = generate_answer(prompt)
    
    print("\nAnswer:\n")
    print(answer)
    
    print("\nSources used:")
    sources = set()
    
    for metadata in results["metadatas"][0]:
        sources.add(metadata["source"])
    
    for source in sources:
        print(f"- {source}")