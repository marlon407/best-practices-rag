import os
import json
from typing import List, Dict

from langchain.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_OPENAPI_INDEX_NAME")

def load_openapi_file(file_path: str) -> List[Document]:
    """
    Carrega um arquivo OpenAPI (JSON) e o converte em documentos LangChain.
    
    Args:
        file_path (str): Caminho para o arquivo OpenAPI JSON
        
    Returns:
        List[Document]: Lista de documentos LangChain
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    documents = []
    
    # Processa informações básicas da API
    info = data.get('info', {})
    base_info = f"API: {info.get('title', '')}\nVersão: {info.get('version', '')}\nDescrição: {info.get('description', '')}"
    documents.append(Document(page_content=base_info))
    
    # Processa servidores
    servers = data.get('servers', [])
    for server in servers:
        server_info = f"Servidor: {server.get('url', '')}\nDescrição: {server.get('description', '')}"
        documents.append(Document(page_content=server_info))
    
    # Processa endpoints e seus métodos
    for path, methods in data.get('paths', {}).items():
        for method, details in methods.items():
            # Cria um documento para cada endpoint
            doc_content = f"Endpoint: {path}\nMétodo: {method.upper()}\n"
            
            # Adiciona descrição do endpoint
            if 'summary' in details:
                doc_content += f"Resumo: {details['summary']}\n"
            if 'description' in details:
                doc_content += f"Descrição: {details['description']}\n"
            
            # Adiciona parâmetros
            if 'parameters' in details:
                doc_content += "\nParâmetros:\n"
                for param in details['parameters']:
                    param_info = f"- {param.get('name', '')} ({param.get('in', '')}): {param.get('description', '')}"
                    doc_content += param_info + "\n"
            
            # Adiciona respostas
            if 'responses' in details:
                doc_content += "\nRespostas:\n"
                for status, response in details['responses'].items():
                    response_info = f"- {status}: {response.get('description', '')}"
                    doc_content += response_info + "\n"
            
            documents.append(Document(page_content=doc_content))
    
    return documents

def split_documents(documents: List[Document]) -> List[Document]:
    """
    Divide os documentos em chunks menores para processamento.
    
    Args:
        documents (List[Document]): Lista de documentos para dividir
        
    Returns:
        List[Document]: Lista de documentos divididos
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    return splitter.split_documents(documents)

def criar_e_preencher_indice(chunks: List[Document]):
    """
    Cria e preenche o índice no Pinecone com os documentos processados.
    
    Args:
        chunks (List[Document]): Lista de documentos divididos
    """
    # Inicializa o cliente Pinecone
    pc = Pinecone(api_key=PINECONE_API_KEY)

    # Cria o índice se não existir
    if PINECONE_INDEX_NAME not in [i.name for i in pc.list_indexes()]:
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )

    # Cria o embedding
    embeddings = OpenAIEmbeddings()

    # Adiciona os documentos ao índice
    vectorstore = PineconeVectorStore.from_documents(
        chunks,
        embedding=embeddings,
        pinecone_api_key=PINECONE_API_KEY,
        index_name=PINECONE_INDEX_NAME
    )
    print("Documentos OpenAPI adicionados ao índice com sucesso!")

if __name__ == "__main__":
    # Caminho para o arquivo OpenAPI
    openapi_file_path = "openapi.json"  # Substitua pelo caminho do seu arquivo
    
    print(f"Processando arquivo OpenAPI: {openapi_file_path}")
    docs = load_openapi_file(openapi_file_path)
    print(f"Total de documentos carregados: {len(docs)}")
    
    chunks = split_documents(docs)
    print(f"Total de chunks após divisão: {len(chunks)}")
    
    criar_e_preencher_indice(chunks) 