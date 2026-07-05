import React, { createContext, useContext, useEffect, useState } from 'react'
import {
  addToCartApi,
  clearCartApi,
  fetchCart,
  removeFromCartApi,
  updateCartItemApi,
} from '../services/api'
import { AuthContext } from './AuthContext.jsx'

export const CartContext = createContext(null)

export function CartProvider({ children }) {
  const { user } = useContext(AuthContext)
  const [items, setItems] = useState([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const refreshCart = async () => {
    if (!user) {
      setItems([])
      setTotal(0)
      return
    }
    setLoading(true)
    try {
      const res = await fetchCart()
      setItems(res.data.items)
      setTotal(res.data.total)
    } catch (e) {
      
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    refreshCart()
    
  }, [user])

  const addToCart = async (productId, quantity = 1) => {
    setError(null)
    try {
      const res = await addToCartApi({ product_id: productId, quantity })
      setItems(res.data.items)
      setTotal(res.data.total)
      return true
    } catch (e) {
      setError(e.response?.data?.detail || 'Could not add item to cart')
      return false
    }
  }

  const updateQuantity = async (productId, quantity) => {
    setError(null)
    try {
      const res = await updateCartItemApi(productId, quantity)
      setItems(res.data.items)
      setTotal(res.data.total)
    } catch (e) {
      setError(e.response?.data?.detail || 'Could not update item')
    }
  }

  const removeItem = async (productId) => {
    const res = await removeFromCartApi(productId)
    setItems(res.data.items)
    setTotal(res.data.total)
  }

  const clearCart = async () => {
    const res = await clearCartApi()
    setItems(res.data.items)
    setTotal(res.data.total)
  }

  const itemCount = items.reduce((sum, i) => sum + i.quantity, 0)

  return (
    <CartContext.Provider
      value={{
        items,
        total,
        itemCount,
        loading,
        error,
        addToCart,
        updateQuantity,
        removeItem,
        clearCart,
        refreshCart,
      }}
    >
      {children}
    </CartContext.Provider>
  )
}

export function useCart() {
  const ctx = useContext(CartContext)
  if (!ctx) throw new Error('useCart must be used within a CartProvider')
  return ctx
}