from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import base
from typing import Optional, List
from pydantic import BaseModel

class Usuario(base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    senha = Column(String, nullable=False)
    tarefas = relationship("Tarefa", back_populates="usuario")

class Tarefa(base):
    __tablename__ = "tarefas"
    id = Column(Integer, primary_key=True, index=True)
    tarefa = Column(String, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))

    usuario = relationship("Usuario", back_populates="tarefas")

class TarefaSchema(BaseModel):
    tarefa: str

class TarefaPublic(BaseModel):
    id: int
    tarefa: str
    usuario_id: int

    class Config:
        orm_mode = True

class UsuarioSchema(BaseModel):
    nome: str
    senha: str

class UsuarioPublic(BaseModel):
    id: int
    nome: str
    tarefas: List[TarefaPublic] = []

    class Config:
        orm_mode = True