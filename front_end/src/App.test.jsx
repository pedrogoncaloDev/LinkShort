import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import App from './App.jsx'
import * as api from './api.js'

describe('App (integração)', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('encurta um link e o mostra na aba Meus Links', async () => {
    vi.spyOn(api, 'shortenUrl').mockResolvedValue({
      shortened_url: 'http://localhost:8000/abc123',
      expires_at: '2026-09-03T12:00:00',
    })
    const user = userEvent.setup()
    render(<App />)

    await user.type(
      screen.getByPlaceholderText('Cole seu URL longo aqui...'),
      'https://exemplo.com/pagina'
    )
    await user.click(screen.getByRole('button', { name: /encurtar/i }))
    await screen.findByText('localhost:8000/abc123')

    await user.click(screen.getByText('Meus Links'))

    expect(screen.getByText('localhost:8000/abc123')).toBeInTheDocument()
    expect(screen.getByText('exemplo.com/pagina')).toBeInTheDocument()
  })
})
