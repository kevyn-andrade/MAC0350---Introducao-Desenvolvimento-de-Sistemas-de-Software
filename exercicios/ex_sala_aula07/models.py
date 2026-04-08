from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class Aluno(SQLModel, table=True):
    nusp: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    idade: int

    # Um aluno pode ter VÁRIAS tarefas → List["Tarefa"]
    tarefas: List["Tarefa"] = Relationship(back_populates="aluno")


class Tarefa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    duracao: int  # duração em minutos, por exemplo

    # Chave estrangeira apontando para aluno.nusp
    aluno_nusp: int = Field(foreign_key="aluno.nusp")

    # Relacionamento reverso: "tarefas" é o nome do atributo em Aluno
    aluno: Optional[Aluno] = Relationship(back_populates="tarefas")
