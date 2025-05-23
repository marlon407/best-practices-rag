from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from query import ask_question
from typing import Dict, List

app = FastAPI()

# Armazena o histórico de cada thread em memória
thread_histories: Dict[str, List] = {}

class QuestionRequest(BaseModel):
    thread_id: str = None
    question: str

class AnswerResponse(BaseModel):
    answer: str

@app.post("/ask", response_model=AnswerResponse)
def ask(request: QuestionRequest):
    if not request.thread_id:
        raise HTTPException(status_code=400, detail="thread_id is required")
    # Recupera ou cria o histórico da thread
    history = thread_histories.setdefault(request.thread_id, [])
    # Adiciona a nova pergunta ao histórico
    # history é uma lista de tuplas (pergunta, resposta)
    resposta = ask_question(request.question, history)
    history.append((request.question, resposta))
    return {"answer": resposta} 