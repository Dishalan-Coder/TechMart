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

 