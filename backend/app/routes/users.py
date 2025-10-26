from fastapi import APIRouter, File, UploadFile
from ..utils.doc_splitter import file_split
from ..database.chroma_connection import store_embeddings
from ..utils.llm_connection import llm_connection


router = APIRouter(
    prefix="/user",
    tags=["items"]
)


@router.post("/upload_file",tags=["users"])
async def upload_file(file:UploadFile):
    file_path = f"F:\Coding Stuff\AI Stuff\RAGChat\static_files\{file.filename}"
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    if file.filename is not None:
        chunks = file_split(file_path=file_path)
        store_embeddings(chunks)
    return "File Uploaded"


@router.post("/chat",tags=["users"])
async def chat_llm(query:str):
    if query is not None:
        try:
            response = await llm_connection(query,file_path)
            return response.content
        except Exception as error:
            return error
