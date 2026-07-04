import React, { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { fetchCategories, fetchProducts } from '../services/api'
import ProductCard from '../components/ProductCard.jsx'

export default function Products() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [products, setProducts] = useState([])
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)

  const search = searchParams.get('search') || ''
  const category = searchParams.get('category') || 'All'
  const sort = searchParams.get('sort') || 'newest'

  useEffect(() => {
    fetchCategories().then((res) => setCategories(['All', ...res.data]))
  }, [])

  useEffect(() => {
    setLoading(true)
    const params = { sort }
    if (search) params.search = search
    if (category && category !== 'All') params.category = category
    fetchProducts(params)
      .then((res) => setProducts(res.data))
      .finally(() => setLoading(false))
  }, [search, category, sort])

  const updateParam = (key, value) => {
    const next = new URLSearchParams(searchParams)
    if (value) next.set(key, value)
    else next.delete(key)
    setSearchParams(next)
  }

  return (
    <div className="products-page">
      <div className="products-header">
        <h1>Electrical Products</h1>
        <p>{products.length} item{products.length !== 1 ? 's' : ''} found</p>
      </div>

      <div className="products-toolbar">
        <input
          type="text"
          placeholder="Search products…"
          defaultValue={search}
          onKeyDown={(e) => {
            if (e.key === 'Enter') updateParam('search', e.target.value)
          }}
          onBlur={(e) => updateParam('search', e.target.value)}
        />
        <select value={category} onChange={(e) => updateParam('category', e.target.value)}>
          {categories.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
        <select value={sort} onChange={(e) => updateParam('sort', e.target.value)}>
          <option value="newest">Newest</option>
          <option value="price_asc">Price: Low to High</option>
          <option value="price_desc">Price: High to Low</option>
          <option value="name_asc">Name: A–Z</option>
        </select>
      </div>

      {loading ? (
        <div className="page-loading">Loading products…</div>
      ) : products.length === 0 ? (
        <div className="empty-state">No products match your filters.</div>
      ) : (
        <div className="product-grid">
          {products.map((p) => (
            <ProductCard key={p.id} product={p} />
          ))}
        </div>
      )}
    </div>
  )
}