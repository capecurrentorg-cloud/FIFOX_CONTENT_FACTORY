import React from 'react'
import './FoxCard.css'

function FoxCard({ fox, onClick }) {
  return (
    <div className="fox-card" onClick={onClick} style={{borderTopColor: fox.color}}>
      <div className="fox-card-header">
        <div className="fox-icon" style={{backgroundColor: fox.color}}>
          🦊
        </div>
        <div className="fox-info">
          <h3 className="fox-name">{fox.name}</h3>
          <p className="fox-role">{fox.role}</p>
        </div>
      </div>
      <div className="fox-card-body">
        <p className="fox-description">{fox.description}</p>
        <div className="fox-meta">
          <span className="fox-age">Age {fox.age}</span>
          <span className="fox-ears" style={{color: fox.color}}>● {fox.earColor} Ears</span>
        </div>
      </div>
      <div className="fox-card-footer">
        <button className="fox-btn">View Details →</button>
      </div>
    </div>
  )
}

export default FoxCard
