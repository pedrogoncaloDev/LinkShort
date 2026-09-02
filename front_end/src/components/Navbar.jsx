export default function Navbar({ activeTab, onTabChange }) {
  return (
    <nav className="navbar">
      <div className="logo">
        <div className="logo-mark">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#052b1c" strokeWidth="2.5" strokeLinecap="round">
            <path d="M9 17H7A5 5 0 0 1 7 7h2" />
            <path d="M15 7h2a5 5 0 1 1 0 10h-2" />
            <line x1="8" y1="12" x2="16" y2="12" />
          </svg>
        </div>
        <span className="logo-text">LinkShort</span>
      </div>

      <div className="tabs">
        <div
          className={`tab ${activeTab === 'encurtar' ? 'active' : ''}`}
          onClick={() => onTabChange('encurtar')}
        >
          Encurtar
        </div>
        <div
          className={`tab ${activeTab === 'meus-links' ? 'active' : ''}`}
          onClick={() => onTabChange('meus-links')}
        >
          Meus Links
        </div>
      </div>
    </nav>
  )
}
