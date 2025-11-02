import logging
import asyncio
from functools import lru_cache
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from database.chroma_connection import get_vector_store
from langchain.memory import ConversationBufferMemory
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

logger = logging.getLogger(__name__)


@lru_cache()
def get_llm():
    """
    Create and cache the ChatOllama model instance.
    """
    logger.info("Initializing LLM model")
    return ChatOllama(
        model="llama3.2-vision:latest",  # could be env-driven too
        temperature=0.3,
        num_predict=100,
    )

@lru_cache()
def get_prompt() -> PromptTemplate:
    """
    Prompt template for RAG QA chain.
    """
    return PromptTemplate.from_template(
        """
        You are a helpful technical assistant.
        Answer the user's question based on the provided context and conversation history.

        Chat History:
        {chat_history}

        Context:
        {context}

        Question:
        {question}

        Answer:
        """
    )


@lru_cache()
def get_rag_chain() -> RetrievalQA:
    """
    Factory for RetrievalQA chain with memory and retriever.
    Cached to avoid reinitialization on every request.
    """
    vectore_store = get_vector_store()
    retriever = vectore_store.as_retriever()

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        input_key="question",
        return_messages=True,
    )

    rag_chain = RetrievalQA.from_chain_type(
        llm=get_llm(),
        retriever=retriever,
        chain_type_kwargs={
            "prompt": get_prompt(),
            "memory": memory,
        },
    )
    logger.info("RAG chain initialized successfully.")
    return rag_chain


async def llm_connection(query:str):
    if not query.strip():
        raise ValueError("Query cannot be empty")
    try:
        rag_chain = get_rag_chain()
        logger.info("Processing query: %s", query)
        response = await asyncio.to_thread(rag_chain.invoke, query)
        result = response.get("result", "")
        logger.info("RAG response generated successfully.")
        return result
    except Exception as e:
        logger.exception("LLM connection failed: %s", e)
        raise RuntimeError(f"Failed to process query: {e}")
        