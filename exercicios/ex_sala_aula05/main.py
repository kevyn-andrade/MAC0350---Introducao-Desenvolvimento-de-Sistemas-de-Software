from fastapi import FastAPI, Request, Depends, HTTPException, Cookie, Response, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()
templates = Jinja2Templates(directory="templates")

usuarios_db = []


class Usuario(BaseModel):
    nome: str
    senha: str
    bio: str


# ─── Rota raiz: página de cadastro ───────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request, "cadastro.html", {})


# ─── Criar usuário (recebe JSON via fetch) ────────────────────────────────────

@app.post("/users")
def criar_usuario(usuario: Usuario):
    for u in usuarios_db:
        if u["nome"] == usuario.nome:
            raise HTTPException(status_code=400, detail="Usuário já cadastrado")
    usuarios_db.append(usuario.dict())
    return {"message": f"Usuário '{usuario.nome}' criado com sucesso!"}


# ─── Página de login ──────────────────────────────────────────────────────────

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {})


@app.post("/login")
def login(nome: str = Form(...), senha: str = Form(...)):
    for u in usuarios_db:
        if u["nome"] == nome and u["senha"] == senha:
            resp = RedirectResponse(url="/home", status_code=303)
            resp.set_cookie(key="session_user", value=nome)
            return resp
    raise HTTPException(status_code=401, detail="Nome ou senha incorretos")


# ─── Dependência: valida o cookie de sessão ───────────────────────────────────

def get_active_user(session_user: Annotated[str | None, Cookie()] = None):
    if not session_user:
        raise HTTPException(status_code=401, detail="Faça login para continuar")
    for u in usuarios_db:
        if u["nome"] == session_user:
            return u
    raise HTTPException(status_code=401, detail="Sessão inválida")


# ─── Página de perfil (rota protegida) ────────────────────────────────────────

@app.get("/home", response_class=HTMLResponse)
def home(request: Request, user: dict = Depends(get_active_user)):
    return templates.TemplateResponse(request, "perfil.html", {"user": user})


@app.post("/logout")
def logout():
    resp = RedirectResponse(url="/login", status_code=303)
    resp.delete_cookie("session_user")
    return resp
