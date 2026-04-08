from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select, SQLModel, create_engine
from models import Aluno, Tarefa

# ─── Configuração do banco ────────────────────────────────────────────────────

arquivo_sqlite = "exercicio_7.db"
url_sqlite = f"sqlite:///{arquivo_sqlite}"
engine = create_engine(url_sqlite)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# ─── App ──────────────────────────────────────────────────────────────────────

app = FastAPI()


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


# ─── Endpoints de Alunos ──────────────────────────────────────────────────────

@app.post("/alunos", response_model=Aluno)
def criar_aluno(aluno: Aluno):
    with Session(engine) as session:
        session.add(aluno)
        session.commit()
        session.refresh(aluno)
        return aluno


@app.get("/alunos", response_model=list[Aluno])
def listar_alunos():
    with Session(engine) as session:
        return session.exec(select(Aluno)).all()


@app.get("/alunos/{aluno_nusp}/tarefas", response_model=list[Tarefa])
def listar_tarefas_do_aluno(aluno_nusp: int):
    with Session(engine) as session:
        aluno = session.get(Aluno, aluno_nusp)
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        # Acessa o relacionamento configurado no modelo
        return aluno.tarefas


# ─── Endpoints de Tarefas ─────────────────────────────────────────────────────

@app.post("/tarefas", response_model=Tarefa)
def criar_tarefa(tarefa: Tarefa):
    with Session(engine) as session:
        # Verifica se o aluno referenciado existe
        aluno = session.get(Aluno, tarefa.aluno_nusp)
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        session.add(tarefa)
        session.commit()
        session.refresh(tarefa)
        return tarefa


@app.get("/tarefas", response_model=list[Tarefa])
def listar_tarefas():
    with Session(engine) as session:
        return session.exec(select(Tarefa)).all()
