import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it } from 'vitest'
import MyLinks from './MyLinks.jsx'

function makeLinks(count) {
  return Array.from({ length: count }, (_, i) => ({
    short: `localhost:8000/link${i}`,
    shortUrl: `http://localhost:8000/link${i}`,
    original: `exemplo.com/${i}`,
    date: '27 ago 2026',
    expiresAt: '03 set 2026, 12:00',
  }))
}

describe('MyLinks', () => {
  it('mostra o estado vazio quando não há links', () => {
    render(<MyLinks links={[]} />)
    expect(screen.getByText(/ainda não encurtou/i)).toBeInTheDocument()
  })

  it('pagina quando há mais links do que cabe numa página', async () => {
    render(<MyLinks links={makeLinks(12)} />)
    const user = userEvent.setup()

    expect(screen.getAllByText(/localhost:8000\/link/)).toHaveLength(5)
    expect(screen.getByText('1 / 3')).toBeInTheDocument()

    await user.click(screen.getByLabelText('Próxima página'))

    expect(screen.getByText('2 / 3')).toBeInTheDocument()
    expect(screen.getByText('localhost:8000/link5')).toBeInTheDocument()
  })

  it('não mostra controles de paginação quando tudo cabe numa página', () => {
    render(<MyLinks links={makeLinks(3)} />)
    expect(screen.queryByLabelText('Próxima página')).not.toBeInTheDocument()
  })
})
