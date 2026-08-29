# LinkShortener

Encurtador de URLs full-stack: **FastAPI + PostgreSQL** no back-end, **React + Vite** no front-end, tudo orquestrado com **Docker Compose** e com deploy automático em Render + Vercel + Neon.

[![CI](https://github.com/pedrogoncaloDev/LinkShortener/actions/workflows/ci.yml/badge.svg)](https://github.com/pedrogoncaloDev/LinkShortener/actions/workflows/ci.yml)

---

## Funcionalidades

- **Encurtar URLs** — gera um código curto de 6 caracteres e devolve o link pronto.
- **Expiração configurável** — de 5 minutos a 1 mês (padrão: 7 dias). Links expirados param de redirecionar.
- **Reaproveitamento de link** — encurtar a mesma URL enquanto o link ainda está válido devolve o código existente em vez de criar outro, evitando inflar o banco.
- **Redirect com fallback** — acessar um código inexistente ou expirado redireciona para o front-end com `?codigo=` na query string, em vez de dar erro.
- **Rate limiting** — `POST /shorten` é limitado a 10 requisições por minuto por IP (`slowapi`), protegendo o endpoint de abuso.
- **"Meus Links" no navegador** — a lista de links criados fica no `localStorage`; não precisa de conta. Inclui paginação e botão de copiar.
- **Validação em dois níveis** — o front dá feedback imediato sobre o prazo de expiração, e o back-end revalida com Pydantic.
- **Health check** — `GET /health` para monitoramento (usado pelo Render).

## Stack

| Camada    | Tecnologias |
|-----------|-------------|
| Back-end  | Python 3.12, FastAPI, Uvicorn, Pydantic, `psycopg2` (SQL puro), `slowapi` |
| Banco     | PostgreSQL 16, migrations com Alembic |
| Front-end | React 18, Vite 5 |
| Testes    | `pytest` + coverage (back-end), Vitest + Testing Library (front-end) |
| Infra     | Docker, Docker Compose, GitHub Actions (CI) |
| Deploy    | Render (back-end), Vercel (front-end), Neon (Postgres) |

## Arquitetura

O back-end segue uma separação em camadas, cada uma com uma responsabilidade:

```
routes.py          → HTTP: rotas, status codes, montagem da resposta
  └─ services/      → regras de negócio: geração de código único, reuso de link, expiração
       └─ repositories/  → acesso ao banco (SQL puro via psycopg2)
```

`config.py` centraliza a leitura de variáveis de ambiente e `db/connection.py` abstrai a conexão (usa `DATABASE_URL` em produção, variáveis `DB_*` em dev/Docker).

### Estrutura do repositório

```
.
├── back_end/
│   ├── main.py                  → cria o app FastAPI, middlewares (CORS, rate limit), debugpy opcional
│   ├── routes.py                → /shorten, /health, /{codigo}
│   ├── schemas.py               → validação de entrada (Pydantic) + limites de expiração
│   ├── config.py                → variáveis de ambiente
│   ├── rate_limit.py            → instância compartilhada do Limiter
│   ├── services/link_service.py → lógica de encurtamento e resolução
│   ├── repositories/link_repository.py → queries da tabela `links`
│   ├── db/connection.py         → conexão psycopg2
│   ├── migrations/              → migrations Alembic
│   ├── tests/                   → testes unitários e de integração
│   └── Dockerfile
├── front_end/
│   ├── src/
│   │   ├── App.jsx              → estado dos links, troca de abas
│   │   ├── api.js               → chamada ao /shorten
│   │   ├── storage.js           → persistência em localStorage
│   │   └── components/          → Navbar, Hero, HowItWorks, MyLinks, Footer
│   ├── vite.config.js
│   └── Dockerfile
├── docker-compose.yml
├── render.yaml                  → blueprint de deploy do back-end
├── DEPLOY.md                    → passo a passo do deploy (Neon → Render → Vercel)
└── .github/workflows/ci.yml
```

### Tabela `links`

| Coluna              | Tipo         | Notas                     |
|---------------------|--------------|---------------------------|
| `id`                | integer PK   |                           |
| `url_original`      | text         | URL de destino            |
| `codigo_encurtado`  | varchar(20)  | único                     |
| `data_criacao`      | timestamp    |                           |
| `data_expiracao`    | timestamp    | comparada com `NOW()` do Postgres |
| `total_acessos`     | integer      | default `0`               |

## API

Base URL local: `http://localhost:8000`

### `POST /shorten`

Cria (ou reaproveita) um link curto. Limitado a **10 req/min por IP**.

**Request**

```json
{
  "url": "https://exemplo.com/pagina/muito/longa?com=parametros",
  "expires_in_minutes": 10080
}
```

`expires_in_minutes` é opcional (padrão `10080` = 7 dias), mínimo `5`, máximo `43200` (30 dias).

**Response `200`**

```json
{
  "shortened_url": "http://localhost:8000/a1b2c3",
  "expires_at": "2026-09-05T14:30:00"
}
```

**Erros:** `400` URL vazia · `422` `expires_in_minutes` fora do intervalo · `429` rate limit excedido.

### `GET /health`

```json
{ "status": "ok" }
```

### `GET /{codigo}`

Redireciona (`307`) para a URL original. Se o código não existir ou estiver expirado, redireciona para `FRONTEND_URL?codigo={codigo}`.

## Rodando localmente

### Com Docker (recomendado)

Sobe banco, back-end e front-end de uma vez:

```bash
cp .env.example .env
docker compose up --build
```

- Front-end: http://localhost:8080
- API: http://localhost:8000
- Postgres: `localhost:5434`

As migrations rodam automaticamente antes do servidor subir (`alembic upgrade head` no `CMD` do Dockerfile).

### Sem Docker

**Back-end** (precisa de um Postgres acessível — ajuste as variáveis `DB_*` no `.env`):

```bash
cd back_end
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
alembic upgrade head
python main.py
```

**Front-end:**

```bash
cd front_end
npm install
npm run dev
```

## Variáveis de ambiente

Copie `.env.example` para `.env` na raiz. Principais:

| Variável           | Usada por  | Descrição |
|--------------------|------------|-----------|
| `VITE_API_URL`     | front-end  | URL do back-end que o front chama |
| `BACKEND_URL`      | back-end   | URL pública do back-end, usada para montar `shortened_url` |
| `FRONTEND_URL`     | back-end   | URL do front-end, usada no redirect de fallback |
| `ALLOWED_ORIGINS`  | back-end   | origens liberadas no CORS (separadas por vírgula) |
| `DB_NAME` / `DB_USER` / `DB_PASSWORD` / `DB_PORT` | ambos | credenciais do Postgres |
| `DATABASE_URL`     | back-end   | connection string completa; em produção tem prioridade sobre as `DB_*` |
| `DEBUG`            | back-end   | `1` liga o `debugpy` (**nunca em produção**) |

## Testes

**Back-end** (usa um Postgres real; o CI sobe um serviço `postgres`):

```bash
cd back_end
pytest --cov=. --cov-report=term-missing
```

**Front-end:**

```bash
cd front_end
npm run test
```

O workflow [`ci.yml`](.github/workflows/ci.yml) roda os dois em todo push e PR para `main`, além de `npm run build`.

## Deploy

Deploy contínuo com integração nativa do GitHub — cada push em `main` reconstrói back-end e front-end automaticamente:

- **Neon** — Postgres gerenciado; fornece a `DATABASE_URL`.
- **Render** — back-end via `render.yaml` (blueprint); roda a migration e sobe o servidor.
- **Vercel** — front-end (root em `front_end/`, preset Vite).

O passo a passo completo, incluindo a ordem para resolver a dependência circular de CORS, está em [DEPLOY.md](DEPLOY.md).
