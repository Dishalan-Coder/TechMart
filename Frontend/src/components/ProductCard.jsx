import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { useCart } from '../context/CartContext.jsx'

const FALLBACK_IMG =
  'data:image/svg+xml;utf8,' +
  encodeURIComponent(
    `<svg xmlns="http://www.w3.org/2000/svg" width="300" height="220"><rect width="100%" height="100%" fill="%23101828"/><text x="50%" y="50%" fill="%23F5B800" font-family="sans-serif" font-size="16" text-anchor="middle">TechMart</text></svg>`
  )

export default function ProductCard({ product }) {
  const { user } = useAuth()
  const { addToCart } = useCart()
  const [status, setStatus] = useState('idle')

  const handleAdd = async (e) => {
    e.preventDefault()
    if (!user) {
      window.location.href = '/login'
      return
    }
    setStatus('loading')
    const ok = await addToCart(product.id, 1)
    setStatus(ok ? 'added' : 'idle')
    if (ok) setTimeout(() => setStatus('idle'), 1500)
  }

  return (
    <Link to={`/products?highlight=${product.id}`} className="product-card">
      <div className="product-card-img">
        <img src={product.image_url || FALLBACK_IMG} alt={product.name} />
        {product.stock === 0 && <span className="badge-oos">Out of stock</span>}
      </div>
      <div className="product-card-body">
        <span className="product-category">{product.category}</span>
        <h3>{product.name}</h3>
        <p className="product-desc">{product.description}</p>
        <div className="product-card-footer">
          <span className="product-price">${product.price.toFixed(2)}</span>
          <button
            className="btn-primary-sm"
            onClick={handleAdd}
            disabled={product.stock === 0 || status === 'loading'}
          >
            {status === 'added' ? 'Added ✓' : 'Add to Cart'}
          </button>
        </div>
      </div>
    </Link>
  )
}