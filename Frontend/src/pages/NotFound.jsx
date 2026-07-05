import React from 'react'
import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <div className="not-found">
      <span className="brand-mark large">⚡</span>
      <h1>404</h1>
      <p>This circuit doesn't connect anywhere. Page not found.</p>
      <Link to="/" className="btn-primary">Back to Home</Link>
    </div>
  )
}