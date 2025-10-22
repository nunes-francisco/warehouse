# 🧩 Projeto: Products API (FastAPI + PostgreSQL + Clean Architecture)

## 🧭 Visão Geral

O projeto **Products API** é uma aplicação **FastAPI** estruturada com **Clean Architecture**, utilizando **PostgreSQL** como banco de dados principal e **Docker Compose** para containerização.
O objetivo é demonstrar boas práticas de design, separação de camadas, validação de dados, testes automatizados e otimização de consultas.

---

## 🎯 Objetivos Principais

1. Criar uma API RESTful para cadastro e consulta de produtos.
2. Aplicar **Clean Architecture** (camadas isoladas e independentes).
3. Utilizar **Pydantic** para validação e tipagem de dados.
4. Persistir dados em **PostgreSQL** com **SQLAlchemy Async**.
5. Containerizar todo o ambiente com **Docker Compose**.
6. Inserir dados de teste via script otimizado (`seed.py`).
7. Implementar **testes automatizados** com **Pytest**.
8. Documentar o planejamento técnico e estrutura do projeto.

---

## 🏗️ Arquitetura e Camadas

### **1. Domain**

- Define as entidades do negócio (`Product`).
- Contém a regra de negócio pura, sem dependências externas.

### **2. Schemas**

- Define os modelos Pydantic usados para entrada e saída (DTOs).
- Garante validação e consistência dos dados.

### **3. Repository**

- Implementa a persistência e abstração de acesso ao banco de dados.
- Usa SQLAlchemy com sessões assíncronas (`AsyncSession`).

### **4. Services**

- Contém a lógica de aplicação (use cases).
- Depende apenas da interface do repositório.

### **5. API**

- Camada de exposição dos endpoints.
- Conecta os serviços ao FastAPI (injeção de dependência via `Depends`).

---

## 🧱 Estrutura Técnica

| Camada                      | Tecnologia              | Função                                          |
| --------------------------- | ----------------------- | ------------------------------------------------- |
| **Backend Framework** | FastAPI                 | Servidor HTTP, rotas e injeção de dependências |
| **ORM**               | SQLAlchemy (async)      | Acesso e manipulação do banco                   |
| **Banco de Dados**    | PostgreSQL              | Armazenamento persistente                         |
| **Infraestrutura**    | Docker + Docker Compose | Orquestração e containers                       |
| **Validação**       | Pydantic                | Tipagem e validação de entrada/saída           |
| **Testes**            | Pytest + HTTPX          | Testes de integração e unidade                  |
| **Scripts**           | seed.py                 | Inserção otimizada de dados de teste            |

---

## 🧩 Banco de Dados

### Tabela: `products`

| Campo           | Tipo          | Descrição                |
| --------------- | ------------- | -------------------------- |
| `id`          | UUID (PK)     | Identificador único       |
| `name`        | TEXT          | Nome do produto            |
| `description` | TEXT          | Descrição opcional       |
| `price`       | NUMERIC(10,2) | Preço do produto          |
| `in_stock`    | BOOLEAN       | Disponibilidade em estoque |
| `created_at`  | TIMESTAMP     | Data de criação          |

### Índices

- `idx_products_name` → acelera buscas por nome
- `idx_products_price` → acelera filtros por faixa de preço

---

## ⚡ Otimização de Consultas

- Uso de **Bulk Insert** no `seed.py` com `execute_values` (melhor desempenho que inserts individuais).
- Criação de **índices após inserção** para ganho de performance em carga inicial.
- Paginação baseada em cursor (`id < last_id`) evita `OFFSET` pesado.
- Pool de conexões configurável via `create_async_engine`.

---

## 🧪 Testes Automatizados

- Framework: **Pytest + HTTPX + Pytest-Asyncio**
- Testes cobrem:
  - Criação de produto (`POST /api/v1/products/`)
  - Consulta (`GET /api/v1/products/{id}`)
  - Atualização (`PATCH`)
  - Listagem (`GET /api/v1/products/`)
  - Exclusão (`DELETE`)

---

## 🚀 Como Executar o Projeto

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/seuusuario/fastapi-products.git
cd fastapi-products
```
