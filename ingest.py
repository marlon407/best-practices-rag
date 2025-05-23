import os
import git

from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from dotenv import load_dotenv


load_dotenv()

REPO_URL = os.getenv("REPO_URL")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

CLONE_DIR = "repo-isb"

def clone_repo():
    if os.path.exists(CLONE_DIR):
        print("Repositório já clonado.")
        return
    print(f"Clonando repositório {REPO_URL}...")
    git.Repo.clone_from(REPO_URL, CLONE_DIR)

def load_documents():
    loader = DirectoryLoader(CLONE_DIR, glob="**/*.md", loader_cls=TextLoader)
    return loader.load()

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    return splitter.split_documents(documents)

def criar_e_preencher_indice(chunks):
    # 1. Inicialize o cliente Pinecone
    pc = Pinecone(api_key=PINECONE_API_KEY)

    # 2. Crie o índice se não existir
    if PINECONE_INDEX_NAME not in [i.name for i in pc.list_indexes()]:
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=1536,  # ajuste conforme o modelo do embedding
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )

    # 3. Crie o embedding
    embeddings = OpenAIEmbeddings()

    # 4. Adicione os documentos ao índice usando o embedding
    vectorstore = PineconeVectorStore.from_documents(
        chunks,
        embedding=embeddings,
        pinecone_api_key=PINECONE_API_KEY,
        index_name=PINECONE_INDEX_NAME
    )
    print("Documentos adicionados ao índice com sucesso!")

if __name__ == "__main__":
    clone_repo()
    docs = load_documents()
    chunks = split_documents(docs)
    criar_e_preencher_indice(chunks)
