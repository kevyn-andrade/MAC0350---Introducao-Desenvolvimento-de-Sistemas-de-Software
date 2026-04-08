from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Estado do contador de curtidas (mantido entre trocas de aba)
curtidas = {"count": 0}

# Ordem das abas para o atalho de teclado (controlado pelo servidor)
abas = ["/curtidas", "/jupiter", "/professor"]
aba_atual = {"index": 0}


# ─── Página principal ─────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {"pagina": "/curtidas"})


# ─── Aba Curtidas ─────────────────────────────────────────────────────────────

@app.get("/curtidas", response_class=HTMLResponse)
def curtidas_page(request: Request):
    if "HX-Request" not in request.headers:
        return templates.TemplateResponse(request, "index.html", {"pagina": "/curtidas"})
    return templates.TemplateResponse(request, "curtidas.html", {"curtidas": curtidas["count"]})


@app.post("/curtir", response_class=HTMLResponse)
def curtir():
    curtidas["count"] += 1
    return HTMLResponse(f'<span id="contador">{curtidas["count"]}</span>')


@app.delete("/curtir", response_class=HTMLResponse)
def zerar_curtidas():
    curtidas["count"] = 0
    return HTMLResponse(f'<span id="contador">{curtidas["count"]}</span>')


# ─── Aba Júpiter ──────────────────────────────────────────────────────────────

@app.get("/jupiter", response_class=HTMLResponse)
def jupiter_page(request: Request):
    if "HX-Request" not in request.headers:
        return templates.TemplateResponse(request, "index.html", {"pagina": "/jupiter"})
    return templates.TemplateResponse(request, "jupiter.html", {})


# ─── Aba Professor ────────────────────────────────────────────────────────────

@app.get("/professor", response_class=HTMLResponse)
def professor_page(request: Request):
    if "HX-Request" not in request.headers:
        return templates.TemplateResponse(request, "index.html", {"pagina": "/professor"})
    return templates.TemplateResponse(request, "professor.html", {})


# ─── Endpoint para atalho de teclado (cicla entre abas) ──────────────────────

@app.get("/proxima-aba", response_class=HTMLResponse)
def proxima_aba(request: Request):
    aba_atual["index"] = (aba_atual["index"] + 1) % len(abas)
    proxima = abas[aba_atual["index"]]
    # Instrui o HTMX a fazer uma nova requisição GET para a próxima aba
    from fastapi.responses import Response
    resp = Response(status_code=200, content="")
    resp.headers["HX-Redirect"] = proxima
    return resp
