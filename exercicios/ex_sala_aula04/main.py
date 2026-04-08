from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()
usuarios = []


class Usuario(BaseModel):
    nome: str
    idade: int


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html") as f:
        return f.read()


@app.post("/users")
async def criar_usuario(usuario: Usuario):
    usuarios.append(usuario.dict())
    return usuarios[-1]


@app.get("/users")
async def ler_usuarios(index: int = None):
    if index is not None:
        if 0 <= index < len(usuarios):
            return usuarios[index]
        return {"erro": f"Índice {index} inválido. Total: {len(usuarios)} usuários."}
    return usuarios


@app.delete("/users")
async def deletar_usuarios():
    usuarios.clear()
    return {"mensagem": "Lista limpa com sucesso"}
