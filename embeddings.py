import chromadb
from chromadb.utils.embedding_functions import EmbeddingFunction
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="./chroma_db")


class MyEmbeddingFunction(EmbeddingFunction):
    def __init__(self):
        self.model = None

    def __call__(self, input):
        if self.model is None:
            self.model = SentenceTransformer("all-MiniLM-L6-v2")

        return self.model.encode(input).tolist()