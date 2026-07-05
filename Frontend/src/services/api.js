import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('techmart_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('techmart_token')
      localStorage.removeItem('techmart_user')
      if (!window.location.pathname.startsWith('/login')) {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

// ---- Auth ----
export const registerUser = (data) => api.post('/auth/register', data)
export const loginUser = (data) => api.post('/auth/login', data)
export const getMe = () => api.get('/users/me')

// ---- Profile ----
export const updateProfile = (data) => api.put('/profile', data)
export const changePassword = (data) => api.put('/profile/password', data)

// ---- Products ----
export const fetchProducts = (params) => api.get('/products', { params })
export const fetchProduct = (id) => api.get(`/products/${id}`)
export const fetchCategories = () => api.get('/products/categories')
export const createProduct = (data) => api.post('/products', data)
export const updateProduct = (id, data) => api.put(`/products/${id}`, data)
export const deleteProduct = (id) => api.delete(`/products/${id}`)
export const uploadProductImage = (formData) =>
  api.post('/products/upload-image', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })

// ---- Cart ----
export const fetchCart = () => api.get('/cart')
export const addToCartApi = (data) => api.post('/cart', data)
export const updateCartItemApi = (productId, quantity) =>
  api.put(`/cart/${productId}`, { quantity })
export const removeFromCartApi = (productId) => api.delete(`/cart/${productId}`)
export const clearCartApi = () => api.delete('/cart')

// ---- Admin ----
export const fetchAdminStats = () => api.get('/admin/stats')
export const fetchAdminUsers = () => api.get('/admin/users')

export default api