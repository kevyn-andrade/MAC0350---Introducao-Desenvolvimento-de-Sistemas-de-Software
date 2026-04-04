from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, Session, select, col
from database import engine, Categoria, Medida, create_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    inicializar_categorias()
    yield

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")

def inicializar_categorias():
    with Session(engine) as session:
        existe = session.exec(select(Categoria)).first()
        if not existe:
            for nome in ["Peso Corporal", "Bíceps", "Supino com Halteres"]:
                session.add(Categoria(nome=nome))
            session.commit()

# --- TELAS ---
@app.get("/", response_class=HTMLResponse)
def ler_pagina_inicial(request: Request):
    with Session(engine) as session:
        medidas = session.exec(select(Medida).order_by(Medida.data.desc())).all()
        categorias = session.exec(select(Categoria)).all()
        return templates.TemplateResponse(request, "index.html",
                                          {"medidas": medidas, "categorias": categorias})

@app.get("/buscar_tela", response_class=HTMLResponse)
def tela_busca(request: Request):
    return templates.TemplateResponse(request, "busca.html", {})

@app.get("/buscar", response_class=HTMLResponse)
def buscar_medidas(request: Request, q: str | None = ""):
    with Session(engine) as session:
        query = select(Medida).join(Categoria)\
                .where(col(Categoria.nome).contains(q))\
                .order_by(Medida.data.desc())
        medidas = session.exec(query).all()

        if not medidas:
            return HTMLResponse(
                content='<tr><td colspan="4" class="empty-state">Nenhum resultado encontrado.</td></tr>'
            )

        html = "".join([
            templates.get_template("linha_medida.html").render({"request": request, "medida": m})
            for m in medidas
        ])
        return HTMLResponse(content=html)

# --- CRUD ---
@app.post("/medidas/", response_class=HTMLResponse)
def criar_medida(request: Request, valor: float = Form(...),
                 categoria_id: int = Form(...), data: str = Form(...)):
    with Session(engine) as session:
        nova = Medida(valor=valor, categoria_id=categoria_id, data=data)
        session.add(nova)
        session.commit()
        session.refresh(nova)
        return templates.TemplateResponse(request, "linha_medida.html", {"medida": nova})

@app.delete("/medidas/{medida_id}", response_class=HTMLResponse)
def deletar_medida(medida_id: int):
    with Session(engine) as session:
        medida = session.get(Medida, medida_id)
        if not medida:
            raise HTTPException(404, "Medida não encontrada")
        session.delete(medida)
        session.commit()
        return HTMLResponse(content="")

@app.get("/medidas/{medida_id}/editar", response_class=HTMLResponse)
def form_editar(request: Request, medida_id: int):
    with Session(engine) as session:
        medida = session.get(Medida, medida_id)
        if not medida:
            raise HTTPException(404, "Medida não encontrada")
        return templates.TemplateResponse(request, "form_editar_medida.html", {"medida": medida})

@app.get("/medidas/{medida_id}/cancelar", response_class=HTMLResponse)
def cancelar_edicao(request: Request, medida_id: int):
    with Session(engine) as session:
        medida = session.get(Medida, medida_id)
        if not medida:
            raise HTTPException(404, "Medida não encontrada")
        return templates.TemplateResponse(request, "linha_medida.html", {"medida": medida})

@app.put("/medidas/{medida_id}", response_class=HTMLResponse)
def atualizar_medida(request: Request, medida_id: int, valor: float = Form(...)):
    with Session(engine) as session:
        medida = session.get(Medida, medida_id)
        if not medida:
            raise HTTPException(404, "Medida não encontrada")
        medida.valor = valor
        session.add(medida)
        session.commit()
        session.refresh(medida)
        return templates.TemplateResponse(request, "linha_medida.html", {"medida": medida})