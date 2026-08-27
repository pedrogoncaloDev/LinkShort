import { useState } from 'react'
import Navbar from './components/Navbar.jsx'
import Hero from './components/Hero.jsx'
import HowItWorks from './components/HowItWorks.jsx'
import MyLinks from './components/MyLinks.jsx'
import Footer from './components/Footer.jsx'
import { shortenUrl } from './api.js'
import { getMyLinks, addMyLink } from './storage.js'

function truncate(str, max = 60) {
  return str.length > max ? str.slice(0, max) + '…' : str
}

function stripProtocol(str) {
  return str.replace(/^https?:\/\/(www\.)?/, '')
}

function formatDateTime(isoString) {
  return new Date(isoString).toLocaleString('pt-BR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export default function App() {
  const [activeTab, setActiveTab] = useState('encurtar')
  const [links, setLinks] = useState(() => getMyLinks())

  const handleShorten = async (originalUrl, expiresInMinutes) => {
    const { shortened_url: shortUrl, expires_at: expiresAt } = await shortenUrl(
      originalUrl,
      expiresInMinutes
    )

    const newLink = {
      short: stripProtocol(shortUrl),
      shortUrl,
      original: truncate(stripProtocol(originalUrl)),
      date: new Date().toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
      }),
      expiresAt: formatDateTime(expiresAt),
    }
    setLinks(addMyLink(newLink))
    return newLink
  }

  return (
    <>
      <Navbar activeTab={activeTab} onTabChange={setActiveTab} />
      {activeTab === 'encurtar' ? (
        <>
          <Hero onShorten={handleShorten} />
          <HowItWorks />
        </>
      ) : (
        <MyLinks links={links} />
      )}
      <Footer />
    </>
  )
}
