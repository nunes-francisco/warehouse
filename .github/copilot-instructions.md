<!-- Copilot / AI agent instructions for the fastapi-products repository -->
# Objetivo rápido

Este repositório implementa uma API simples de produtos usando FastAPI + SQLAlchemy (async). Use este arquivo para orientar agentes automatizados a entender a arquitetura, convenções e como executar/ testá-lo localmente.

## Visão geral da arquitetura

- Entrada: `main.py` — instancia um `FastAPI` e inclui o router `src.api.v1.products` em `/api/v1/products`.
- Camadas principais:
  - `src/api/v1/` — endpoints (APIRouter). Ex: `products.py` usa dependências para criar `ProductService`.
  - `src/services/` — lógica de aplicação (orquestra repository operations). Ex: `ProductService` chama `ProductRepository`.
  - `src/repository/` — acesso ao banco (SQLAlchemy ORM async). Ex: `ProductRepository` usa `AsyncSession` e `sqlalchemy.future.select`.
  - `src/domain/` — modelos ORM (declarative Base). Ex: `models.py` declara `Product` com índices e tipos Postgres.
  - `src/schemas/` — Pydantic models (input/output). Ex: `ProductCreate`, `ProductUpdate`, `Product`.
  - `src/core/` — infra (config e factory de sessão): `settings.py` (env via pydantic-settings) e `database.py` (engine async, `get_session`).

## Convenções e padrões específicos

- Async-first: todas as operações de DB e endpoints usam async/await. Preferir `AsyncSession` e `select()`.
- DI via Depends: routers criam serviços com fixtures como `get_session` (veja `products.get_product_service`).
- Pydantic > ORM mapping: schemas usam `ConfigDict(from_attributes=True)` e os repositórios instanciam models do domínio com `Product(**product.model_dump())`.
- Atualização parcial: `ProductUpdate` usa `model_dump(exclude_unset=True)` no repositório para aplicar somente campos enviados.
- Testes usam SQLite em arquivo (`sqlite+aiosqlite:///./test.db`) com override da dependência `get_session` em `tests/conftest.py`.

## Pontos de atenção / integração

- Banco: `src/core/settings.py` lê `DATABASE_URL` via `.env` — localmente o projeto espera um Postgres (ex.: `postgresql+asyncpg://...`) ou pode usar sqlite para testes.
- Tipos Postgres: `src/domain/models.py` usa `UUID` do `sqlalchemy.dialects.postgresql` — quando usar SQLite nos testes, o código funciona, mas esteja atento a diferenças de tipos.
- Migrations: `alembic` está listada em `requirements.txt` mas não há diretório `alembic` no repositório. Se for necessário, criar configuração antes de rodar migrations.

## Como executar (dev)

- Instalar deps (repositório usa `requirements.txt`):
  - pip install -r requirements.txt
- Rodar localmente:
  - uvicorn main:app --reload --host 0.0.0.0 --port 8000
- Executar com Docker (Dockerfile contem CMD padrão uvicorn):
  - docker build -t fastapi-products . && docker run -p 8000:8000 fastapi-products

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

Se você ver erros sobre `pytest_asyncio` ou outras libs faltando, confirme que instalou `requirements.txt` no virtualenv ativo.

## Execução rápida (local)

```bash
# rodar o server de desenvolvimento
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# exemplo de chamada HTTP (usando httpie or curl)
curl -s http://127.0.0.1:8000/api/v1/products | jq
```

## Como rodar testes

- Tests usam pytest + pytest-asyncio; fixtures em `tests/conftest.py` criam banco sqlite `test.db` e fazem override de `get_session`.
- Com ambiente configurado:
  - pytest -q

Se os testes falharem por dependências de DB (ex.: usando Postgres), use a configuração de `DATABASE_URL` correta ou execute dentro de um ambiente com Postgres.

## Exemplos de padrões identificados (use nos PRs/edits)

- Criar serviço em router via dependency factory:
  - ver `src/api/v1/products.py:get_product_service()` — cria `ProductRepository(session)` e injeta `ProductService`.
- Repositório async padrão:
  - `get()`: usa `select(Product).filter(Product.id == product_id)` e `scalars().first()`.
  - `create()`: instancia domain model com `Product(**product.model_dump())`, add, commit, refresh.
  - `update()`: usa `model_dump(exclude_unset=True)` para mudanças parciais.

## O que evitar / limitações detectadas

- Não assumir que `alembic` está configurado — não há scripts de migration aqui.
- Evitar mudanças que alterem a assinatura das dependências (`get_session`) sem atualizar `tests/conftest.py`.

## Onde procurar mais informações

- Entradas principais: `main.py`, `src/api/v1/products.py`, `src/services/product_service.py`, `src/repository/product_repository.py`, `src/core/database.py`, `tests/conftest.py`.

---
Se quiser, eu posso ajustar o tom (mais técnico, mais sucinto) ou incluir snippets automáticos de PRs/commits para tarefas comuns (ex.: adicionar migration alembic, adicionar suporte a SQLite em produção, etc.).
