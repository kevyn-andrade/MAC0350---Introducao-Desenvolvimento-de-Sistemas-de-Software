from sqlmodel import SQLModel, Field, Relationship, create_engine
from typing import Optional, List

engine = create_engine("sqlite:///./medidas.db", connect_args={"check_same_thread": False})

class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(unique=True, index=True)
    medidas: List["Medida"] = Relationship(back_populates="categoria")

class Medida(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    valor: float
    data: str
    categoria_id: Optional[int] = Field(default=None, foreign_key="categoria.id")
    categoria: Optional[Categoria] = Relationship(back_populates="medidas")

def create_db():
    SQLModel.metadata.create_all(engine)