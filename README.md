# Warehouse Products API

![](/Users/francisconunes/Projects/warehouse/assets/capa.png)

Este repositório implementa uma API simples de produtos usando FastAPI + SQLAlchemy (async) e Pydantic.

## Visão geral da arquitetura

- Entrada: `main.py` — instancia um `FastAPI` e inclui o router `src.api.v1.products` em `/api/v1/products`.
- Camadas principais:
  - `src/api/v1/` — endpoints (APIRouter). Ex: `products.py` usa dependências para criar `ProductService`.
  - `src/services/` — lógica de aplicação (orquestra repository operations). Ex: `ProductService` chama `ProductRepository`.
  - `src/repository/` — acesso ao banco (SQLAlchemy ORM async). Ex: `ProductRepository` usa `AsyncSession` e `sqlalchemy.future.select`.
  - `src/domain/` — modelos ORM (declarative Base). Ex: `models.py` declara `Product` com índices e tipos Postgres.
  - `src/schemas/` — Pydantic models (input/output). Ex: `ProductCreate`, `ProductUpdate`, `Product`.
  - `src/core/` — infra (config e factory de sessão): `settings.py` (env via pydantic-settings) e `database.py` (engine async, `get_session`).

## Endpoints da API

A base da URL para todos os endpoints é `/api/v1/products`.

| Método | Rota | Descrição | Payload (Corpo) | Resposta |
| --- | --- | --- | --- | --- |
| POST | `/` | Cria um novo produto. | `ProductCreate` | `Product` |
| GET | `/` | Retorna uma lista de produtos. | - | `List[Product]` |
| GET | `/{product_id}` | Retorna um produto pelo ID. | - | `Product` |
| PATCH | `/{product_id}` | Atualiza um produto pelo ID. | `ProductUpdate` | `Product` |
| DELETE | `/{product_id}` | Deleta um produto pelo ID. | - | `Product` |
| GET | `/search/` | Busca produtos pelo nome. | - | `List[Product]` |

### Schemas

-   **ProductCreate**:
    -   `name: str`
    -   `description: str`
    -   `price: float`
-   **ProductUpdate**:
    -   `name: Optional[str]`
    -   `description: Optional[str]`
    -   `price: Optional[float]`
-   **Product**:
    -   `id: uuid.UUID`
    -   `name: str`
    -   `description: str`
    -   `price: float`
    -   `created_at: datetime`
    -   `updated_at: datetime`

## Como executar (dev)

- Instalar deps (repositório usa `requirements.txt`):
  - `pip install -r requirements.txt`
- Rodar localmente:
  - `uvicorn main:app --reload --host 0.0.0.0 --port 8000`
- Executar com Docker (Dockerfile contem CMD padrão uvicorn):
  - `docker build -t fastapi-products . && docker run -p 8000:8000 fastapi-products`

### Setup local (macOS - zsh)

Recomendado: crie e ative um virtualenv, atualize pip e instale dependências. Exemplo de comandos para zsh (macOS):

```bash
# usar python3 (compatível com Dockerfile: 3.9+)
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Notas importantes:
- Se preferir `python` mapeado para outra versão, use o caminho completo do binário (ex.: `/usr/local/bin/python3`).
- O projeto lê `DATABASE_URL` via `pydantic-settings` em `src/core/settings.py`. Para rodar contra Postgres configure `.env` com:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
```

- Para testes locais a suíte de testes já usa um SQLite temporário (`sqlite+aiosqlite:///./test.db`) configurado em `tests/conftest.py`.

## Como rodar testes (local)

Depois de ativar o virtualenv e instalar dependências:

```bash
# rodar a suíte de testes (pytest + pytest-asyncio)
pytest -q
```
