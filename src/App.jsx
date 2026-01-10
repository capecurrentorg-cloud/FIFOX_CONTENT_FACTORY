import React, { useState } from 'react'
import { foxes, foxCategories } from './data/foxes'
import FoxCard from './components/FoxCard'
import './App.css'

function App() {
  const [selectedTab, setSelectedTab] = useState('all')
  const [selectedFox, setSelectedFox] = useState(null)

  const filterFoxes = () => {
    if (selectedTab === 'all') return foxes
    if (selectedTab === 'operations') return foxes.filter(f => foxCategories.operations.includes(f.id))
    if (selectedTab === 'content') return foxes.filter(f => !foxCategories.operations.includes(f.id))
    return foxes
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <h1>🦊 FIFOX Command Center</h1>
          <p className="subtitle">AI-Powered Restaurant Automation System</p>
        </div>
      </header>

      <nav className="nav-tabs">
        <button 
          className={selectedTab === 'all' ? 'tab active' : 'tab'}
          onClick={() => setSelectedTab('all')}
        >
          All Foxes ({foxes.length})
        </button>
        <button 
          className={selectedTab === 'operations' ? 'tab active' : 'tab'}
          onClick={() => setSelectedTab('operations')}
        >
          Operations (5)
        </button>
        <button 
          className={selectedTab === 'content' ? 'tab active' : 'tab'}
          onClick={() => setSelectedTab('content')}
        >
          Content Creators (8)
        </button>
      </nav>

      <main className="main-content">
        <div className="fox-grid">
          {filterFoxes().map(fox => (
            <FoxCard 
              key={fox.id} 
              fox={fox} 
              onClick={() => setSelectedFox(fox)}
            />
          ))}
        </div>
      </main>

      {selectedFox && (
        <div className="modal-overlay" onClick={() => setSelectedFox(null)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setSelectedFox(null)}>✕</button>
            <div className="modal-content">
              <div className="modal-header" style={{borderLeftColor: selectedFox.color}}>
                <h2>{selectedFox.name} {selectedFox.nickname && `"${selectedFox.nickname}"`}</h2>
                <p className="modal-role">{selectedFox.role}</p>
              </div>
              <div className="modal-body">
                <div className="modal-section">
                  <h3>About</h3>
                  <p><strong>Age:</strong> {selectedFox.age}</p>
                  <p><strong>Background:</strong> {selectedFox.background}</p>
                  <p><strong>Fox Ears:</strong> {selectedFox.earColor}</p>
                </div>
                <div className="modal-section">
                  <h3>Personality</h3>
                  <p>{selectedFox.personality}</p>
                </div>
                <div className="modal-section">
                  <h3>Description</h3>
                  <p>{selectedFox.description}</p>
                </div>
                <div className="modal-section">
                  <h3>Key Features</h3>
                  <ul>
                    {selectedFox.features.map((feature, idx) => (
                      <li key={idx}>✓ {feature}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      <footer className="footer">
        <p>FIFOX Restaurant Automation • $299/month • Replaces 3+ Employees</p>
        <p className="footer-small">Running a restaurant should feel like playing a video game. Click buttons. Stuff happens. No stress.</p>
      </footer>
    </div>
  )
}

export default App
