import React from 'react'
import { useCart } from '../context/CartContext.jsx'

export default function CartItem({ item }) {
  const { updateQuantity, removeItem } = useCart()

  return (
    <div className="cart-item">
      <img
        src={
          item.image_url ||
          'data:image/svg+xml;utf8,' +
            encodeURIComponent(
              `<svg xmlns="http://www.w3.org/2000/svg" width="90" height="90"><rect width="100%" height="100%" fill="%23101828"/></svg>`
            )
        }
        alt={item.name}
      />
      <div className="cart-item-info">
        <h4>{item.name}</h4>
        <span className="cart-item-price">${item.price.toFixed(2)} each</span>
      </div>
      <div className="cart-item-qty">
        <button onClick={() => updateQuantity(item.product_id, item.quantity - 1)}>−</button>
        <span>{item.quantity}</span>
        <button
          onClick={() => updateQuantity(item.product_id, item.quantity + 1)}
          disabled={item.quantity >= item.stock}
        >
          +
        </button>
      </div>
      <div className="cart-item-total">${(item.price * item.quantity).toFixed(2)}</div>
      <button className="cart-item-remove" onClick={() => removeItem(item.product_id)} aria-label="Remove item">
        ✕
      </button>
    </div>
  )
}