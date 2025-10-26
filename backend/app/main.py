from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import users
import uvicorn




app = FastAPI(description="A file RAG application")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)



@app.get("/")
async def root():
    return {"message":"Welcome to File RAG Application"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

