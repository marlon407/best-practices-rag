from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from query import ask_question
from typing import Dict, List
from dynamo_utils import save_message, get_thread_history
import uuid

app = FastAPI()

class QuestionRequest(BaseModel):
    thread_id: str = None
    question: str

class AnswerResponse(BaseModel):
    answer: str

@app.post("/ask", response_model=AnswerResponse)
def ask(request: QuestionRequest):
    thread_id = request.thread_id
    if not request.thread_id:
        thread_id = str(uuid.uuid4())
    # Busca histórico do DynamoDB
    history = get_thread_history(thread_id)
    print(history)
    resposta = ask_question(request.question, history)
    # Salva a nova interação
    save_message(thread_id, request.question, resposta)
    return {"answer": resposta, "thread_id": thread_id} 