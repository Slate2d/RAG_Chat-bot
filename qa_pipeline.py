from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM


class QAPipeline:
    def __init__(self, vector_store):
        self.llm = OllamaLLM(model="llama3.1", base_url="http://localhost:11434")
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=vector_store.as_retriever()
        )

    def answer_question(self, question, context):
        prompt = f"You are a smart agent. A question would be asked to you and relevant information would be provided.\
            Your task is to answer the question and use the information provided. Question - {question}. Relevant Information - {context}"
        return self.qa_chain.invoke(prompt)
