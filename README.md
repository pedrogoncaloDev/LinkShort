# LinkShort — Redesign (React + Vite)

## Como rodar

```bash
npm install
npm run dev
```

Abre em `http://localhost:8080` (porta já configurada no `vite.config.js` pra bater
com a que você estava usando).

## Estrutura

```
src/
  App.jsx                  → junta todas as seções e guarda o estado dos links
  index.css                → todos os estilos (tokens de cor/tipografia no topo)
  components/
    Navbar.jsx              → logo + abas Encurtar / Meus Links
    Hero.jsx                → headline, input de encurtar, animação de assinatural
    HowItWorks.jsx          → 3 passos
    LinksTable.jsx          → prévia da tabela "Meus Links"
    Footer.jsx
```

## O que já é funcional

- O input do Hero tem estado real (`useState`) e, ao enviar, gera um código
  curto aleatório e insere a linha no topo da tabela "Meus Links" — troque
  `handleShorten` no `App.jsx` pela sua chamada de API quando tiver o backend.
- O botão de copiar na tabela já usa `navigator.clipboard`.
- As abas do Navbar trocam `activeTab`, mas a troca de conteúdo entre
  "Encurtar" e "Meus Links" ainda não está ligada — hoje a página mostra
  tudo em scroll único. Se você quiser duas telas separadas (como no
  protótipo original), me avisa que eu separo em rotas.

## Próximos passos sugeridos

1. Trocar `generateCode` / a lista mockada em `App.jsx` pela sua API real.
2. Se for usar rotas de verdade, dá pra trocar as abas por `react-router-dom`.
3. Os ícones estão como SVG inline — se preferir, dá pra trocar por
   `lucide-react` sem mudar o layout.
