import asyncio
import logging
from typing import List, Iterable
from functools import lru_cache
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
import chromadb

logger = logging.getLogger(__name__)

@lru_cache
def get_chroma_client():
    logger.info("Creating / reusing Chroma PersistentClient")
    client = chromadb.PersistentClient(path=r"backend\app\chroma_db")
    return client

@lru_cache
def get_vector_store():
    client = get_chroma_client()
    embedding = OllamaEmbeddings(
        model="nomic-embed-text"
    )
    vectore_store = Chroma(
        client=client,
        collection_name="RAGChat",
        embedding_function=embedding
    )
    return vectore_store

def store_embeddings(documents, batch_size=5000):
    docs_list:List = list(documents)
    vector_store = get_vector_store()
    for i in range(0, len(docs_list),batch_size):
        batch = documents[i:i+batch_size]
        vector_store.add_documents(batch)

    logger.info("Stored vector embeddings")
    


