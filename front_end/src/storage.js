const STORAGE_KEY = 'linkshort:my-links'

export function getMyLinks() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

export function addMyLink(link) {
  const updated = [link, ...getMyLinks()]
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updated))
  } catch {
    // localStorage indisponível (modo privado, quota cheia, etc.) — segue só em memória
  }
  return updated
}
