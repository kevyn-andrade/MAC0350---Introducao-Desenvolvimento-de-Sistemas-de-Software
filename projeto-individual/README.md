# 💪 Meu Físico

Aplicação web para rastreamento de medidas corporais e evolução física, desenvolvida como projeto individual da disciplina **MAC0350 - Introdução ao Desenvolvimento de Sistemas de Software**.

## 📋 Funcionalidades

- Registro de medidas corporais por categoria (Peso Corporal, Bíceps, etc.)
- Histórico de medidas ordenado por data
- Edição e exclusão de registros
- Busca de medidas por categoria
- Interface responsiva para mobile e desktop

## 🛠️ Tecnologias utilizadas

| Camada | Tecnologia |
|--------|-----------|
| Back-end | [FastAPI](https://fastapi.tiangolo.com/) |
| Banco de dados | SQLite + [SQLModel](https://sqlmodel.tiangolo.com/) |
| Front-end | HTML, CSS, [Tailwind CSS](https://tailwindcss.com/) |
| Interatividade | [HTMX](https://htmx.org/) |
| Templates | Jinja2 |

## 📁 Estrutura do projeto

```
projeto-individual/
├── main.py                      # Aplicação FastAPI e rotas
├── database.py                  # Modelos do banco de dados
├── templates/
│   ├── base.html                # Layout base
│   ├── index.html               # Tela de registro
│   ├── busca.html               # Tela de busca
│   ├── linha_medida.html        # Componente de linha da tabela
│   └── form_editar_medida.html  # Formulário de edição inline
└── requirements.txt
```

## 🗄️ Modelos do banco de dados

**Categoria** — armazena os tipos de medida (ex: Peso Corporal, Bíceps)

**Medida** — armazena cada registro com valor, data e referência à categoria

Relação: `Categoria` →(1:N)→ `Medida`

## ▶️ Como executar

**1. Clone o repositório:**
```bash
git clone https://github.com/kevyn-andrade/MAC0350---Introducao-Desenvolvimento-de-Sistemas-de-Software.git
cd MAC0350---Introducao-Desenvolvimento-de-Sistemas-de-Software/projeto-individual
```

**2. Crie e ative o ambiente virtual:**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
```

**3. Instale as dependências:**
```bash
pip install fastapi uvicorn sqlmodel jinja2 python-multipart
```

**4. Inicie o servidor:**
```bash
uvicorn main:app --reload
```

**5. Acesse no navegador:**
```
http://localhost:8000
```

## 🖥️ Telas

- **`/`** → Registrar nova medida e ver histórico
- **`/buscar_tela`** → Buscar medidas por categoria

## ✅ Requisitos atendidos

- [x] Duas ou mais telas responsivas
- [x] FastAPI como framework back-end
- [x] Dois modelos com relação no banco de dados
- [x] HTMX para operações CRUD (hx-post, hx-get, hx-put, hx-delete)
- [x] Busca de objetos por categoria
