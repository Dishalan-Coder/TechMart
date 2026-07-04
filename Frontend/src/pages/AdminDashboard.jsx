import React, { useEffect, useState } from 'react'
import {
  createProduct,
  deleteProduct,
  fetchAdminStats,
  fetchAdminUsers,
  fetchCategories,
  fetchProducts,
  updateProduct,
  uploadProductImage,
} from '../services/api'

const EMPTY_FORM = {
  name: '', description: '', price: '', category: '', brand: '', stock: '', image_url: '',
}

export default function AdminDashboard() {
  const [tab, setTab] = useState('overview')
  const [stats, setStats] = useState(null)
  const [products, setProducts] = useState([])
  const [users, setUsers] = useState([])
  const [categories, setCategories] = useState([])
  const [form, setForm] = useState(EMPTY_FORM)
  const [editingId, setEditingId] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [msg, setMsg] = useState('')

  const loadOverview = () => fetchAdminStats().then((res) => setStats(res.data))
  const loadProducts = () => fetchProducts({}).then((res) => setProducts(res.data))
  const loadUsers = () => fetchAdminUsers().then((res) => setUsers(res.data))
  const loadCategories = () => fetchCategories().then((res) => setCategories(res.data))

  useEffect(() => {
    loadOverview()
    loadProducts()
    loadCategories()
  }, [])

  useEffect(() => {
    if (tab === 'users') loadUsers()
    if (tab === 'products') loadProducts()
    if (tab === 'overview') loadOverview()
  }, [tab])

  const resetForm = () => {
    setForm(EMPTY_FORM)
    setEditingId(null)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setMsg('')
    const payload = {
      ...form,
      price: parseFloat(form.price),
      stock: parseInt(form.stock || '0', 10),
      image_url: form.image_url || null,
    }
    try {
      if (editingId) {
        await updateProduct(editingId, payload)
        setMsg('Product updated.')
      } else {
        await createProduct(payload)
        setMsg('Product created.')
      }
      resetForm()
      loadProducts()
      loadCategories()
      loadOverview()
    } catch (err) {
      setMsg(err.response?.data?.detail || 'Failed to save product.')
    }
  }

  const handleEdit = (p) => {
    setEditingId(p.id)
    setForm({
      name: p.name, description: p.description, price: p.price, category: p.category,
      brand: p.brand || '', stock: p.stock, image_url: p.image_url || '',
    })
    setTab('products')
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const handleDelete = async (id) => {
    if (!confirm('Delete this product?')) return
    await deleteProduct(id)
    loadProducts()
    loadOverview()
  }

  const handleFileChange = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    setUploading(true)
    try {
      const fd = new FormData()
      fd.append('file', file)
      const res = await uploadProductImage(fd)
      setForm((f) => ({ ...f, image_url: res.data.url }))
    } catch {
      setMsg('Image upload failed.')
    } finally {
      setUploading(false)
    }
  }

 return (
    <div className="admin-page">
      <h1>Admin Dashboard</h1>

      <div className="tabs">
        <button className={tab === 'overview' ? 'active' : ''} onClick={() => setTab('overview')}>Overview</button>
        <button className={tab === 'products' ? 'active' : ''} onClick={() => setTab('products')}>Products</button>
        <button className={tab === 'users' ? 'active' : ''} onClick={() => setTab('users')}>Users</button>
      </div>

      {tab === 'overview' && stats && (
        <div className="stats-grid">
          <div className="stat-card"><span>{stats.total_products}</span><p>Total Products</p></div>
          <div className="stat-card"><span>{stats.total_users}</span><p>Registered Users</p></div>
          <div className="stat-card"><span>{stats.total_categories}</span><p>Categories</p></div>
          <div className="stat-card warn"><span>{stats.low_stock}</span><p>Low Stock (≤5)</p></div>
          <div className="stat-card danger"><span>{stats.out_of_stock}</span><p>Out of Stock</p></div>
          <div className="stat-card"><span>${stats.inventory_value.toLocaleString()}</span><p>Inventory Value</p></div>
        </div>
      )}

      {tab === 'products' && (
        <div className="admin-products">
          <div className="card">
            <h3>{editingId ? 'Edit Product' : 'Add New Product'}</h3>
            {msg && <div className="alert-info">{msg}</div>}
            <form onSubmit={handleSubmit} className="product-form">
              <label>Name
                <input required value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
              </label>
              <label>Description
                <textarea required rows={2} value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
              </label>
              <div className="form-row">
                <label>Price ($)
                  <input required type="number" step="0.01" min="0" value={form.price} onChange={(e) => setForm({ ...form, price: e.target.value })} />
                </label>
                <label>Stock
                  <input required type="number" min="0" value={form.stock} onChange={(e) => setForm({ ...form, stock: e.target.value })} />
                </label>
              </div>
              <div className="form-row">
                <label>Category
                  <input required list="cat-list" value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })} />
                  <datalist id="cat-list">
                    {categories.map((c) => <option key={c} value={c} />)}
                  </datalist>
                </label>
                <label>Brand
                  <input value={form.brand} onChange={(e) => setForm({ ...form, brand: e.target.value })} />
                </label>
              </div>
              <label>Product Image
                <input type="file" accept="image/*" onChange={handleFileChange} />
                {uploading && <span className="hint">Uploading…</span>}
                {form.image_url && <img src={form.image_url} alt="preview" className="img-preview" />}
              </label>
              <div className="form-actions">
                <button type="submit" className="btn-primary">{editingId ? 'Update Product' : 'Add Product'}</button>
                {editingId && <button type="button" className="btn-ghost" onClick={resetForm}>Cancel</button>}
              </div>
            </form>
          </div>

          <div className="card">
            <h3>All Products ({products.length})</h3>
            <div className="table-wrap">
              <table>
                <thead>
                  <tr><th>Name</th><th>Category</th><th>Price</th><th>Stock</th><th></th></tr>
                </thead>
                <tbody>
                  {products.map((p) => (
                    <tr key={p.id}>
                      <td>{p.name}</td>
                      <td>{p.category}</td>
                      <td>${p.price.toFixed(2)}</td>
                      <td className={p.stock === 0 ? 'text-danger' : p.stock <= 5 ? 'text-warn' : ''}>{p.stock}</td>
                      <td className="table-actions">
                        <button className="btn-ghost sm" onClick={() => handleEdit(p)}>Edit</button>
                        <button className="btn-ghost sm danger" onClick={() => handleDelete(p.id)}>Delete</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {tab === 'users' && (
        <div className="card">
          <h3>Registered Users ({users.length})</h3>
          <div className="table-wrap">
            <table>
              <thead>
                <tr><th>Name</th><th>Email</th><th>Role</th><th>Phone</th></tr>
              </thead>
              <tbody>
                {users.map((u) => (
                  <tr key={u.id}>
                    <td>{u.name}</td>
                    <td>{u.email}</td>
                    <td><span className={`role-pill ${u.role}`}>{u.role}</span></td>
                    <td>{u.phone || '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}