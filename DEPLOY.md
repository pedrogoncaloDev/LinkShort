# Deploy — Frontend (Vercel) + Backend (Render) + Postgres (Neon)

O CI (`.github/workflows/ci.yml`) roda os testes em todo push/PR pra `main`.
O deploy em si **não** passa pelo GitHub Actions — Vercel e Render têm
integração nativa com o GitHub e fazem deploy automático a cada push na
branch conectada. É a prática padrão (evita guardar tokens de deploy no
repo) e mais simples de manter.

Ordem recomendada: **Neon → Render → Vercel → voltar no Render**. O
backend precisa do domínio do frontend (CORS) e vice-versa, então dá pra
resolver a dependência circular assim.

## 1. Neon (Postgres)

1. Crie um projeto em [neon.tech](https://neon.tech).
2. Copie a **connection string** (aba "Connection Details") — já vem com
   `?sslmode=require`. Guarde, vai virar `DATABASE_URL` no Render.

## 2. Render (backend)

1. No dashboard do Render, "New" → "Blueprint", conecte este repositório.
   Ele lê o `render.yaml` da raiz automaticamente.
2. Depois de criado o serviço, em Environment, preencha:
   - `DATABASE_URL` → a connection string do Neon.
   - `BACKEND_URL` → a URL pública que o Render atribuiu ao serviço
     (ex.: `https://linkshortener-backend.onrender.com`).
   - `FRONTEND_URL` e `ALLOWED_ORIGINS` → deixe um placeholder por
     enquanto (ex.: `https://localhost`), volta aqui depois do passo 3.
3. O deploy roda `alembic upgrade head` automaticamente antes de subir o
   servidor (mesmo `CMD` do Dockerfile usado em dev) — a tabela `links` é
   criada sozinha no banco do Neon no primeiro deploy.
4. Confirme que subiu: `GET https://<seu-servico>.onrender.com/health`
   deve responder `{"status":"ok"}`.

## 3. Vercel (frontend)

1. "Add New Project" na Vercel, conecte o repositório.
2. Em "Root Directory", selecione `front_end` (é um monorepo — a Vercel
   não acha o `package.json` sozinha na raiz).
3. Framework Preset: Vite (detectado automaticamente).
4. Em Environment Variables, adicione `VITE_API_URL` = a URL do Render
   do passo 2 (ex.: `https://linkshortener-backend.onrender.com`).
5. Deploy. Anote o domínio que a Vercel atribuiu
   (ex.: `https://linkshortener.vercel.app`).

## 4. Volte no Render e feche o CORS

Em Environment no Render, atualize:

- `FRONTEND_URL` → o domínio da Vercel.
- `ALLOWED_ORIGINS` → o mesmo domínio da Vercel (várias origens seriam
  separadas por vírgula, mas aqui é só uma).

Salvar dispara um novo deploy automaticamente.

## Depois disso

- Todo push em `main` que passar no CI já vai automaticamente:
  Render reconstrói o backend (roda migração + sobe o servidor), Vercel
  reconstrói o frontend. Nenhum dos dois espera o CI "passar" antes de
  fazer deploy — são gatilhos independentes. Se quiser que o deploy só
  aconteça depois do CI verde, dá pra configurar "Required status checks"
  na branch `main` (Settings → Branches no GitHub) — isso não impede o
  deploy automático, mas impede merge de PR com CI quebrado.
- **Nunca defina `DEBUG=1` no Render** — liga o `debugpy` escutando numa
  porta exposta publicamente. O código já não define isso por padrão.
