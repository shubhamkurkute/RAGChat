import logging
from pathlib import Path
from fastapi import APIRouter, File, UploadFile, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from utils.doc_splitter import file_split
from database.chroma_connection import store_embeddings
from utils.llm_connection import llm_connection

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/user",
    tags=["users"]
)

class ChatReqeust(BaseModel):
    query:str


def _process_and_store(path: Path):
        """Background processing: Split and embed file"""
        try:
            chunks = file_split(path)
            if not chunks:
                logger.warning("No chunks returned from %s", path)
                return
            store_embeddings(chunks)
            logger.info("Completed embedding for file %s", path.name)
        except Exception as e:
            logger.exception("Failed to process file %s: %s", path, e)


@router.post("/upload_file",tags=["users"])
async def upload_file(file:UploadFile, background_task:BackgroundTasks=None):

    if not file:
        raise HTTPException(status_code=400, detail = "Invalid filename")
    
    try:
        file_path = f"F:\Coding Stuff\AI Stuff\RAGChat\static_files\{file.filename}"
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
      
        
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Could not upload the file")
    

    if background_task is not None:
        background_task.add_task(_process_and_store, Path(file_path))
        return JSONResponse(status_code=201, content={"message": "File uploaded and processed"})
    else:
        import asyncio
        await asyncio.to_thread(_process_and_store, Path(file_path))
        return JSONResponse(status_code=201, content={"message": "File uploaded and processed"})
        


@router.post("/chat",tags=["users"])
async def chat_llm(request:ChatReqeust):
    if request.query is not None:
        try:
            response = await llm_connection(request.query)
            return JSONResponse(content={"response":response}, status_code=200)
        except Exception as error:
            logger.exception(error)
            return JSONResponse(content={"error":error}, status_code=500)
    else:
        raise HTTPException(status_code=400, detail="Query parameter is required and cannot be empty")
