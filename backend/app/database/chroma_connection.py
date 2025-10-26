from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
import chromadb

client = chromadb.PersistentClient(path=r"backend\app\chroma_db")
embedding = OllamaEmbeddings(
    model="nomic-embed-text"
)

vectore_store = Chroma(
    client=client,
    collection_name="RAGChat",
    embedding_function=embedding
)

def store_embeddings(documents, batch_size=5000):
   for i in range(0, len(documents),5000):
      batch = documents[i:i+batch_size]
      vectore_store.add_documents(documents)


