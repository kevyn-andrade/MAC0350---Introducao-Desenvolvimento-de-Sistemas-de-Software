import math
from contextlib import asynccontextmanager

from fastapi import FastAPI, Form, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, SQLModel, col, create_engine, func, select

from Models import Aluno

# ─── Banco de dados ───────────────────────────────────────────────────────────

arquivo_sqlite = "HTMX2.db"
url_sqlite = f"sqlite:///{arquivo_sqlite}"
engine = create_engine(url_sqlite)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def initFunction(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=initFunction)
templates = Jinja2Templates(directory="Templates")

LIMITE = 10  # alunos por página


# ─── Helpers ──────────────────────────────────────────────────────────────────

def buscar_alunos(busca: str, pagina: int) -> list[Aluno]:
    """Retorna a página correta de alunos filtrada pelo nome."""
    offset = (pagina - 1) * LIMITE
    with Session(engine) as session:
        query = (
            select(Aluno)
            .where(col(Aluno.nome).contains(busca))
            .order_by(Aluno.nome)
            .offset(offset)
            .limit(LIMITE)
        )
        return session.exec(query).all()


def contar_alunos(busca: str) -> int:
    """Conta quantos alunos correspondem ao filtro (para calcular total de páginas)."""
    with Session(engine) as session:
        query = select(func.count()).select_from(Aluno).where(col(Aluno.nome).contains(busca))
        return session.exec(query).one()


# ─── Rotas ────────────────────────────────────────────────────────────────────

@app.get("/busca", response_class=HTMLResponse)
def busca(request: Request):
    return templates.TemplateResponse(request, "index.html", {})


@app.get("/lista", response_class=HTMLResponse)
def lista(request: Request, busca: str | None = "", pagina: int = 1):
    """
    Endpoint principal da lista.
    Recebe 'busca' (texto) e 'pagina' (número) como query parameters.
    """
    busca = busca or ""
    total = contar_alunos(busca)
    total_paginas = max(1, math.ceil(total / LIMITE))

    # Garante que a página pedida é válida
    pagina = max(1, min(pagina, total_paginas))

    alunos = buscar_alunos(busca, pagina)

    return templates.TemplateResponse(request, "lista.html", {
        "alunos": alunos,
        "pagina": pagina,
        "total_paginas": total_paginas,
        "busca": busca,
    })


@app.get("/editarAlunos", response_class=HTMLResponse)
def editar_alunos(request: Request):
    return templates.TemplateResponse(request, "options.html", {})


@app.post("/novoAluno", response_class=HTMLResponse)
def criar_aluno(nome: str = Form(...)):
    with Session(engine) as session:
        novo = Aluno(nome=nome)
        session.add(novo)
        session.commit()
        session.refresh(novo)
        return HTMLResponse(f"<p>✅ '{novo.nome}' adicionado (ID {novo.id})</p>")


@app.delete("/deletaAluno", response_class=HTMLResponse)
def deletar_aluno(id: int):
    with Session(engine) as session:
        aluno = session.get(Aluno, id)
        if not aluno:
            raise HTTPException(404, "Aluno não encontrado")
        session.delete(aluno)
        session.commit()
        return HTMLResponse(f"<p>🗑️ Aluno ID {id} removido</p>")


@app.put("/atualizaAluno", response_class=HTMLResponse)
def atualizar_aluno(id: int = Form(...), novoNome: str = Form(...)):
    with Session(engine) as session:
        aluno = session.get(Aluno, id)
        if not aluno:
            raise HTTPException(404, "Aluno não encontrado")
        nome_antigo = aluno.nome
        aluno.nome = novoNome
        session.commit()
        session.refresh(aluno)
        return HTMLResponse(f"<p>✏️ '{nome_antigo}' → '{novoNome}'</p>")


@app.delete("/apagar", response_class=HTMLResponse)
def apagar():
    """Apaga todos os alunos do banco de dados."""
    with Session(engine) as session:
        session.exec(select(Aluno)).all()
        alunos = session.exec(select(Aluno)).all()
        for aluno in alunos:
            session.delete(aluno)
        session.commit()
    return HTMLResponse("<h1>Site deletado com sucesso!</h1>")
