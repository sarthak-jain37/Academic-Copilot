import chromadb
import os
from chromadb.utils.embedding_functions import EmbeddingFunction
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()
chroma_client = chromadb.PersistentClient(path="./chroma_db")

token = os.getenv("HF_TOKEN")

model = SentenceTransformer("all-MiniLM-L6-v2", token=token)

class MyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input):
        return model.encode(input).tolist()