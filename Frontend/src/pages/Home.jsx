import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchCategories, fetchProducts } from '../services/api'
import ProductCard from '../components/ProductCard.jsx'

const CATEGORY_ICONS = {
  'Circuit Protection': '🛡️',
  'Lighting': '💡',
  'Wiring & Cables': '🔌',
  'Switches & Sockets': '🔘',
  'Tools & Testers': '🧰',
  'Appliances': '🌀',
}

export default function Home() {
  const [featured, setFeatured] = useState([])
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([fetchProducts({ sort: 'newest' }), fetchCategories()])
      .then(([prodRes, catRes]) => {
        setFeatured(prodRes.data.slice(0, 8))
        setCategories(catRes.data)
      })
      .finally(() => setLoading(false))
  }, [])

  return (
    <div>
      <section className="hero">
        <div className="hero-inner">
          <span className="eyebrow">Certified electrical supplies</span>
          <h1>Power every project, from panel to plug.</h1>
          <p>
            Wiring, breakers, lighting, and tools sourced from trusted brands —
            in stock and ready to ship for contractors, engineers, and DIYers.
          </p>
          <div className="hero-actions">
            <Link to="/products" className="btn-primary">Shop Products</Link>
            <Link to="/register" className="btn-ghost light">Create an account</Link>
          </div>
        </div>
        <div className="hero-graphic" aria-hidden="true">
          <div className="volt-ring">
            <span>⚡</span>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <h2>Shop by category</h2>
        </div>
        <div className="category-grid">
          {categories.map((cat) => (
            <Link key={cat} to={`/products?category=${encodeURIComponent(cat)}`} className="category-card">
              <span className="category-icon">{CATEGORY_ICONS[cat] || '⚡'}</span>
              <span>{cat}</span>
            </Link>
          ))}
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <h2>Newly added</h2>
          <Link to="/products" className="link-more">View all →</Link>
        </div>
        {loading ? (
          <div className="page-loading">Loading products…</div>
        ) : (
          <div className="product-grid">
            {featured.map((p) => (
              <ProductCard key={p.id} product={p} />
            ))}
          </div>
        )}
      </section>

      <section className="perks">
        <div className="perk"><span>🚚</span><div><h4>Fast dispatch</h4><p>Same-day shipping on in-stock items.</p></div></div>
        <div className="perk"><span>✅</span><div><h4>Certified stock</h4><p>All products meet safety standards.</p></div></div>
        <div className="perk"><span>💬</span><div><h4>Expert support</h4><p>Talk to our electrical specialists.</p></div></div>
      </section>
    </div>
  )
}