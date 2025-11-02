import logging
import asyncio
from pathlib import Path
from langchain_community.document_loaders import (
    PyMuPDFLoader,
    TextLoader,
    Docx2txtLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)



splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=25)

def _load_file(file_path:Path):
    
    if  file_path.suffix.lower() == ".pdf":
        pdf_loader = PyMuPDFLoader(file_path=file_path)
        return pdf_loader
    elif file_path.suffix.lower() == ".docx":
        docx_loader = Docx2txtLoader(file_path=file_path)
        return docx_loader
    elif file_path.suffix.lower() == ".txt":
        text_loader = TextLoader(file_path=file_path)
        return text_loader

def file_split(file_path:Path):

    try:
        logger.info("Loading and splitting file: %s", file_path)
        loader = _load_file(file_path)
        documents = loader.load()
        chunks = splitter.split_documents(documents)
        logger.info("Split %s into %d chunks", file_path, len(chunks))
        return chunks
    except Exception as e:
        logger.exception("Failed to split file: %s", e)
        raise RuntimeError(f"Failed to process {file_path}: {e}")


        

