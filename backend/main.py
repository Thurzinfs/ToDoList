from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

class Tarefa(BaseModel):
    texto: str

tarefas = []

@app.get("/api/tarefas")
async def listar():
    return tarefas

@app.post("/api/tarefas")
async def adicionar_tarefa(tarefa: Tarefa):
    tarefas.append(tarefa.texto)
    return {"mensagem": "Sucesso ao adicionar tarefa."}

@app.delete("/api/tarefas/{indice}")
async def remover_tarefa(indice: int):
    if 0 <= indice < len(tarefas):
        tarefas.pop(indice)
        return {"mensagem": "Tarefa removida com sucesso."}
    return {"mensagem": "erro ao remover tarefa."}