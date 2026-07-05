import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { useCart } from '../context/CartContext.jsx'

export default function Navbar() {
  const { user, logout } = useAuth()
  const { itemCount } = useCart()
  const navigate = useNavigate()
  const [menuOpen, setMenuOpen] = useState(false)

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <header className="navbar">
      <div className="navbar-inner">
        <Link to="/" className="brand">
          <span className="brand-mark">⚡</span>
          <span className="brand-name">TechMart<em>Electrical</em></span>
        </Link>

        <button
          className="nav-toggle"
          onClick={() => setMenuOpen((o) => !o)}
          aria-label="Toggle navigation"
        >
          <span />
          <span />
          <span />
        </button>

        <nav className={`nav-links ${menuOpen ? 'open' : ''}`}>
          <Link to="/" onClick={() => setMenuOpen(false)}>Home</Link>
          <Link to="/products" onClick={() => setMenuOpen(false)}>Products</Link>
          {user?.role === 'admin' && (
            <Link to="/admin" onClick={() => setMenuOpen(false)}>Dashboard</Link>
          )}
          <Link to="/cart" className="nav-cart" onClick={() => setMenuOpen(false)}>
            Cart
            {itemCount > 0 && <span className="cart-badge">{itemCount}</span>}
          </Link>

          {user ? (
            <div className="nav-user">
              <Link to="/profile" onClick={() => setMenuOpen(false)} className="nav-profile">
                {user.name.split(' ')[0]}
              </Link>
              <button className="btn-ghost" onClick={handleLogout}>Logout</button>
            </div>
          ) : (
            <div className="nav-user">
              <Link to="/login" className="btn-ghost" onClick={() => setMenuOpen(false)}>Login</Link>
              <Link to="/register" className="btn-primary-sm" onClick={() => setMenuOpen(false)}>Sign Up</Link>
            </div>
          )}
        </nav>
      </div>
    </header>
  )
}