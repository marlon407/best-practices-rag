from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from query import ask_question
from typing import Dict, List
from dynamo_utils import save_message, get_thread_history
import uuid


app = FastAPI()

app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],  # Em produção, especifique o domínio do frontend
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
class QuestionRequest(BaseModel):
    thread_id: str = None
    question: str

class AnswerResponse(BaseModel):
    answer: str
    thread_id: str

@app.post("/ask", response_model=AnswerResponse)
def ask(request: QuestionRequest):
    print("thread_id", request.thread_id)
    thread_id = request.thread_id
    if not request.thread_id:
        thread_id = str(uuid.uuid4())
    history = get_thread_history(thread_id)
    resposta = ask_question(request.question, history)
    save_message(thread_id, request.question, resposta)
    return {"answer": resposta, "thread_id": thread_id} 