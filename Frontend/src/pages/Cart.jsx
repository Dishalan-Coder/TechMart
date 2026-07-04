import React from 'react'
import { Link } from 'react-router-dom'
import { useCart } from '../context/CartContext.jsx'
import CartItem from '../components/CartItem.jsx'

export default function Cart() {
  const { items, total, loading, error, clearCart } = useCart()

  if (loading) return <div className="page-loading">Loading cart…</div>

  return (
    <div className="cart-page">
      <h1>Your Cart</h1>
      {error && <div className="alert-error">{error}</div>}

      {items.length === 0 ? (
        <div className="empty-state">
          <p>Your cart is empty.</p>
          <Link to="/products" className="btn-primary">Browse Products</Link>
        </div>
      ) : (
        <div className="cart-layout">
          <div className="cart-items">
            {items.map((item) => (
              <CartItem key={item.product_id} item={item} />
            ))}
            <button className="btn-ghost" onClick={clearCart}>Clear cart</button>
          </div>

          <div className="cart-summary">
            <h3>Order Summary</h3>
            <div className="summary-row">
              <span>Subtotal</span>
              <span>${total.toFixed(2)}</span>
            </div>
            <div className="summary-row">
              <span>Shipping</span>
              <span>Free</span>
            </div>
            <div className="summary-row total">
              <span>Total</span>
              <span>${total.toFixed(2)}</span>
            </div>
            <button className="btn-primary full" onClick={() => alert('Checkout is not implemented in this demo.')}>
              Proceed to Checkout
            </button>
          </div>
        </div>
      )}
    </div>
  )
}