from langchain_community.vectorstores import Pinecone as LangchainPinecone

from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough

import os

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

def load_vector_store():
    emb = OpenAIEmbeddings()
    return PineconeVectorStore(pinecone_api_key=PINECONE_API_KEY, index_name=INDEX_NAME, embedding=emb)


def ask_question(query: str):
    db = load_vector_store()
    retriever = db.as_retriever()

    llm = ChatOpenAI(model="gpt-4o-mini")

    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    answer = qa_chain.invoke({"query": query})

    return answer["result"]

if __name__ == "__main__":
    while True:
        q = input("Digite sua pergunta (ou 'sair'): ")
        if q.lower() == "sair":
            break
        print(ask_question(q))
