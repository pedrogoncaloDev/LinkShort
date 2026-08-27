import { useState } from 'react'

const PAGE_SIZE = 5

export default function MyLinks({ links }) {
  const [page, setPage] = useState(1)

  const totalPages = Math.max(1, Math.ceil(links.length / PAGE_SIZE))
  const currentPage = Math.min(page, totalPages)
  const start = (currentPage - 1) * PAGE_SIZE
  const pageLinks = links.slice(start, start + PAGE_SIZE)

  const handleCopy = (link) => {
    navigator.clipboard?.writeText(link.shortUrl || `https://${link.short}`)
  }

  return (
    <section className="section section-my-links">
      <div className="section-head">
        <div className="section-eyebrow">Meus Links</div>
        <h2>Tudo organizado num só lugar</h2>
        <p>
          Guardados neste navegador — não é preciso conta, mas se você trocar
          de dispositivo ou limpar os dados, a lista some.
        </p>
      </div>

      <div className="table-card">
        <div className="table-header">
          <h3>Links criados aqui</h3>
        </div>

        {links.length === 0 ? (
          <div className="table-empty">
            Você ainda não encurtou nenhum link neste navegador.
          </div>
        ) : (
          <>
            <div className="row head">
              <div>Link curto</div>
              <div>Destino</div>
              <div>Criado em</div>
              <div></div>
            </div>

            {pageLinks.map((link) => (
              <div className="row" key={link.short}>
                <div className="short">
                  {link.shortUrl ? (
                    <a href={link.shortUrl} target="_blank" rel="noreferrer">
                      {link.short}
                    </a>
                  ) : (
                    link.short
                  )}
                </div>
                <div className="original">{link.original}</div>
                <div className="date">{link.date}</div>
                <div
                  className="copy-btn"
                  onClick={() => handleCopy(link)}
                  title="Copiar link"
                >
                  ⧉
                </div>
              </div>
            ))}

            {totalPages > 1 && (
              <div className="table-footer">
                <span className="table-footer-info">
                  {start + 1}–{Math.min(start + PAGE_SIZE, links.length)} de {links.length}
                </span>
                <div className="pagination">
                  <button
                    type="button"
                    className="page-btn"
                    disabled={currentPage === 1}
                    onClick={() => setPage(currentPage - 1)}
                    aria-label="Página anterior"
                  >
                    ‹
                  </button>
                  <span className="pagination-info">
                    {currentPage} / {totalPages}
                  </span>
                  <button
                    type="button"
                    className="page-btn"
                    disabled={currentPage === totalPages}
                    onClick={() => setPage(currentPage + 1)}
                    aria-label="Próxima página"
                  >
                    ›
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </section>
  )
}
