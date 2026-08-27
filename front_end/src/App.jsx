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

export default function App() {
  const [activeTab, setActiveTab] = useState('encurtar')
  const [links, setLinks] = useState(() => getMyLinks())

  const handleShorten = async (originalUrl) => {
    const { shortened_url: shortUrl } = await shortenUrl(originalUrl)

    const newLink = {
      short: stripProtocol(shortUrl),
      shortUrl,
      original: truncate(stripProtocol(originalUrl)),
      date: new Date().toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
      }),
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
