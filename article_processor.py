import requests
import re
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import numpy as np


class ArticleProcessor:
    def __init__(self, url_forbes):
        self.url_forbes = url_forbes
        self.article_chunks = []
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chunk_embeddings = {}

    def fetch_article(self):
        """Fetch and parse the article from url"""
        response = requests.get(self.url_forbes)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            article_content = soup.find('div', {'class': 'article-body'})
            if article_content:
                text = article_content.text.strip()
                self.article_chunks = self.split_article(text)
        else:
            print(f"Error fetching article: {response.status_code}")

    def split_article(self, text):
        """Split the article into chunks"""
        chunks = re.split(r'\d+\.\s', text)
        return [chunk.strip() for chunk in chunks if chunk.strip()]

    def compute_embeddings(self):
        """Compute embeddings for the article chunks"""
        self.chunk_embeddings = {i: self.embedding_model.encode(chunk) for i, chunk in enumerate(self.article_chunks)}

    def find_relevant_chunk(self, question):
        """Find the chunk most relevant to the question"""
        question_embedding = self.embedding_model.encode(question)
        scores = {i: np.dot(question_embedding, emb) for i, emb in self.chunk_embeddings.items()}
        best_chunk_id = max(scores, key=scores.get)
        return self.article_chunks[best_chunk_id]
