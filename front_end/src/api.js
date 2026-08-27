const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function shortenUrl(url, expiresInMinutes) {
  const response = await fetch(`${API_URL}/shorten`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url, expires_in_minutes: expiresInMinutes }),
  })

  if (!response.ok) {
    const data = await response.json().catch(() => null)
    if (response.status === 429) {
      throw new Error('Muitos links criados em pouco tempo. Espere um minuto e tente de novo.')
    }
    throw new Error(data?.detail || data?.error || 'Não foi possível encurtar o link.')
  }

  return response.json()
}
