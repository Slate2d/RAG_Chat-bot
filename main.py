import streamlit as st
from article_processor import ArticleProcessor
from ollama_api import OllamaAPI

URL_FORBES = 'https://www.forbes.com/sites/entertainment/article/famous-authors/'
URL_OLLAMA = 'http://ollama:11434/api/generate'
article_processor = ArticleProcessor(URL_FORBES)
ollama_api = OllamaAPI(URL_OLLAMA)

article_processor.fetch_article()
article_processor.compute_embeddings()

st.title("Question Answering System")

question = st.text_input("Ask a question:")

if question:
    context = article_processor.find_relevant_chunk(question)
    ollama_api.generate_response(question, context)
    full_response = ollama_api.get_full_response()

    st.write(full_response)
