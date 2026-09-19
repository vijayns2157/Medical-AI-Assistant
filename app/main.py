from fastapi import FastAPI
from pydantic import BaseModel

from app.rag import ask_question


app = FastAPI(
    title="Medical Coding AI Assistant",
    version="1.0.0",
)


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    sources: list


@app.get("/health")
def health():
    return {
        "status": "ok",
    }


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    return ask_question(request.question)