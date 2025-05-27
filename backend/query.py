from langchain_community.vectorstores import Pinecone as LangchainPinecone

from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import ConversationalRetrievalChain

import os

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

def load_vector_store():
    emb = OpenAIEmbeddings()
    return PineconeVectorStore(pinecone_api_key=PINECONE_API_KEY, index_name=INDEX_NAME, embedding=emb)


def ask_question(query: str, history=None):
    if history is None:
        history = []
    db = load_vector_store()
    retriever = db.as_retriever()
    llm = ChatOpenAI(model="gpt-4o-mini")

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=False
    )
    result = qa_chain({"question": query, "chat_history": history})
    return result["answer"]

if __name__ == "__main__":
    history = []
    while True:
        q = input("Digite sua pergunta (ou 'sair'): ")
        if q.lower() == "sair":
            break
        resposta = ask_question(q, history)
        print(resposta)
        history.append((q, resposta))
 