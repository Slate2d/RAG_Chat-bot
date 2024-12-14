import streamlit as st
from article_processor import ArticleFetcher
from embeddings import EmbeddingHandler
from qa_pipeline import QAPipeline

URL_FORBES = 'https://www.forbes.com/sites/entertainment/article/famous-authors/'

st.set_page_config(page_title="RAG Chatbot")
st.title("🤖 RAG Chatbot")

status_placeholder = st.empty()

status_placeholder.write("Fetching article...")
try:
    fetcher = ArticleFetcher(URL_FORBES)
    article_chunks = fetcher.fetch()
    status_placeholder.success(f"Loaded {len(article_chunks)} chunks from the article.")
except Exception as e:
    status_placeholder.error(f"Error fetching article: {e}")
    st.stop()

status_placeholder.write("Embedding article chunks...")
embedding_handler = EmbeddingHandler()
embedding_handler.create_vector_store(article_chunks)
status_placeholder.success("Embeddings created and stored successfully.")

status_placeholder.write("Ready to answer your questions!")

st.markdown("### Ask a Question")
question = st.text_input("Type your question below:")

if question:
    context = embedding_handler.search(question)

    if context:
        st.markdown("**Relevant Context Found:**")
        st.code(context, language='markdown')

        qa_pipeline = QAPipeline(embedding_handler.vector_store)
        answer = qa_pipeline.answer_question(question, context)

        st.markdown("### Answer")
        st.write(answer["result"])
    else:
        st.warning("No relevant context found for the question.")


