export default function MyLinks({ links }) {
  const handleCopy = (link) => {
    navigator.clipboard?.writeText(link.shortUrl || `https://${link.short}`)
  }

  return (
    <section className="section">
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

            {links.map((link) => (
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
          </>
        )}
      </div>
    </section>
  )
}
