import { useState } from 'react'

export default function Hero({ onShorten }) {
  const [url, setUrl] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState(null)
  const [result, setResult] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!url.trim() || isSubmitting) return

    setIsSubmitting(true)
    setError(null)
    setResult(null)
    try {
      const newLink = await onShorten(url.trim())
      setUrl('')
      setResult(newLink)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleCopy = () => {
    if (result) navigator.clipboard?.writeText(result.shortUrl)
  }

  return (
    <section className="hero">
      <div>
        <div className="eyebrow">
          <span className="eyebrow-dot"></span> Sem cadastro para começar
        </div>

        <h1>
          Links longos ficam <span>curtos</span>. Em um clique.
        </h1>

        <p className="sub">
          Cole a URL, personalize se quiser, e compartilhe. Seus links ficam
          organizados e rastreáveis num só lugar — sem enrolação.
        </p>

        <form className="shorten-card" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Cole seu URL longo aqui..."
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
          <button type="submit" className="btn-primary" disabled={isSubmitting}>
            {isSubmitting ? 'Encurtando...' : 'Encurtar →'}
          </button>
        </form>

        {error && <p className="form-error">{error}</p>}

        <div className="fine-print">
          <span>
            <span className="dot"></span> Rápido
          </span>
          <span>
            <span className="dot"></span> Seguro
          </span>
          <span>
            <span className="dot"></span> Gratuito
          </span>
        </div>

        {result && (
          <div className="shorten-result">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
              <path d="M9 17H7A5 5 0 0 1 7 7h2" />
              <path d="M15 7h2a5 5 0 1 1 0 10h-2" />
              <line x1="8" y1="12" x2="16" y2="12" />
            </svg>
            <a href={result.shortUrl} target="_blank" rel="noreferrer">
              {result.short}
            </a>
            <button type="button" className="copy-btn" onClick={handleCopy} title="Copiar link">
              ⧉
            </button>
          </div>
        )}
      </div>

      <ShrinkDemo />
    </section>
  )
}

function ShrinkDemo() {
  return (
    <div className="demo">
      <div className="demo-label">Como funciona, na prática</div>

      <div className="url-row">
        <svg className="bar-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <rect x="3" y="4" width="18" height="16" rx="2" />
          <line x1="3" y1="9" x2="21" y2="9" />
        </svg>
        <span className="url-long">
          https://www.exemplo.com.br/produtos/categoria/eletronicos?ref=campanha&utm=agosto2026
        </span>
      </div>

      <div className="cut-track">
        <div className="cut-line"></div>
        <div className="scissor">✂️</div>
      </div>

      <div className="url-short">
        <svg className="link-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
          <path d="M9 17H7A5 5 0 0 1 7 7h2" />
          <path d="M15 7h2a5 5 0 1 1 0 10h-2" />
          <line x1="8" y1="12" x2="16" y2="12" />
        </svg>
        <span>lnk.sh/x7F2a</span>
      </div>
    </div>
  )
}
