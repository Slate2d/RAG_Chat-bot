from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingHandler:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = None

    def create_vector_store(self, texts):
        self.vector_store = Chroma.from_texts(
            texts=texts,
            embedding=self.embeddings
        )

    def search(self, query, top_k=3):
        if not self.vector_store:
            raise ValueError("Vector store is not initialized.")
        return self.vector_store.similarity_search(query, k=top_k)
