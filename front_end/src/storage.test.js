import { beforeEach, describe, expect, it } from 'vitest'
import { addMyLink, getMyLinks } from './storage.js'

describe('storage', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('retorna lista vazia quando nada foi salvo ainda', () => {
    expect(getMyLinks()).toEqual([])
  })

  it('adiciona um link no início da lista e persiste', () => {
    const first = { short: 'a', shortUrl: 'http://x/a' }
    const second = { short: 'b', shortUrl: 'http://x/b' }

    addMyLink(first)
    const result = addMyLink(second)

    expect(result).toEqual([second, first])
    expect(getMyLinks()).toEqual([second, first])
  })

  it('não quebra se o conteúdo salvo estiver corrompido', () => {
    localStorage.setItem('linkshort:my-links', 'não é json')
    expect(getMyLinks()).toEqual([])
  })
})
