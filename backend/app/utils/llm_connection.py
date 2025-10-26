from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from ..database.chroma_connection import vectore_store
 

model = ChatOllama(
    model="llama3.2-vision:latest",
    temperature=0.3,
    num_predict=100
    
    
)


async def llm_connection(query:str):
    context = vectore_store.similarity_search(query,filter={"source":}
    prompt = f''' You are a helfpul technical assistant. 
          Answer the question using the following context : {context}
          
          Question : {query}'''
    try:
        resonse = model.invoke(prompt)
        return resonse
    except Exception as error:
        return error