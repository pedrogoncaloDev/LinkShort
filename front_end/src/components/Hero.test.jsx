import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import Hero from './Hero.jsx'

describe('Hero', () => {
  it('rejeita um prazo abaixo do mínimo sem chamar onShorten', async () => {
    const onShorten = vi.fn()
    const user = userEvent.setup()
    render(<Hero onShorten={onShorten} />)

    await user.type(screen.getByPlaceholderText('Cole seu URL longo aqui...'), 'https://exemplo.com')
    await user.clear(screen.getByLabelText('Expira em'))
    await user.type(screen.getByLabelText('Expira em'), '2')
    await user.selectOptions(screen.getByRole('combobox'), 'minutos')
    await user.click(screen.getByRole('button', { name: /encurtar/i }))

    expect(onShorten).not.toHaveBeenCalled()
    expect(screen.getByText(/entre 5 minutos e 1 mês/i)).toBeInTheDocument()
  })

  it('envia a url com o prazo convertido em minutos e mostra o resultado', async () => {
    const onShorten = vi.fn().mockResolvedValue({
      shortUrl: 'http://localhost:8000/abc123',
      short: 'localhost:8000/abc123',
      expiresAt: '03 set 2026, 12:00',
    })
    const user = userEvent.setup()
    render(<Hero onShorten={onShorten} />)

    await user.type(
      screen.getByPlaceholderText('Cole seu URL longo aqui...'),
      'https://exemplo.com/pagina'
    )
    await user.click(screen.getByRole('button', { name: /encurtar/i }))

    // padrão: 7 dias = 60 * 24 * 7 minutos
    expect(onShorten).toHaveBeenCalledWith('https://exemplo.com/pagina', 60 * 24 * 7)
    expect(await screen.findByText('localhost:8000/abc123')).toBeInTheDocument()
    expect(screen.getByText(/expira em 03 set 2026, 12:00/i)).toBeInTheDocument()
  })

  it('mostra a mensagem de erro quando onShorten falha', async () => {
    const onShorten = vi.fn().mockRejectedValue(new Error('Não foi possível encurtar o link.'))
    const user = userEvent.setup()
    render(<Hero onShorten={onShorten} />)

    await user.type(screen.getByPlaceholderText('Cole seu URL longo aqui...'), 'https://exemplo.com')
    await user.click(screen.getByRole('button', { name: /encurtar/i }))

    expect(await screen.findByText('Não foi possível encurtar o link.')).toBeInTheDocument()
  })
})
