from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from models import TarefaSchema, TarefaPublic, UsuarioSchema, UsuarioPublic, Usuario, Tarefa
from database import get_session
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import select

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

router = APIRouter(
    prefix="/api",
    tags=['/api']
)

@router.post(
    path='/registar',
    response_model=UsuarioPublic,
)
def criar_usuario(
    usuario: UsuarioSchema,
    session: Session = Depends(get_session)
):
    user = Usuario(**usuario.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.post(
    path='/tarefa',
    response_model=TarefaPublic
)
def registra_tarefa(
    tarefa: TarefaSchema,
    session: Session = Depends(get_session)
):
    regis_tarefa = Tarefa(**tarefa.model_dump())
    session.add(regis_tarefa)
    session.commit()
    session.refresh(regis_tarefa)
    return regis_tarefa

@router.post(
    path='/login',
    response_model=UsuarioPublic
)
def login(
    dados: UsuarioSchema,
    session: Session = Depends(get_session)
):
    usuario = session.query(Usuario).filter_by(nome=dados.nome, senha=dados.senha).first()
    if not usuario:
        raise HTTPException(status_code=404, detail='User not Found')
    return usuario

@router.get(
    path='/tarefas/{usuario_id}',
    response_model=List[TarefaPublic]
)
def listar_tarefas(
    usuario_id: int,
    session: Session = Depends(get_session),

):
    query = session.scalars(select(Tarefa).where(Tarefa.usuario_id == usuario_id))
    tarefas = query.all()
    return tarefas

@router.delete(
    path='/remove/{tarefa_id}'
)
def delete_tarefa(
    tarefa_id: int,
    session: Session = Depends(get_session)
):
    tarefa = session.get(Tarefa, tarefa_id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa not Found")
    session.delete(tarefa)
    session.commit()

app.include_router(router)