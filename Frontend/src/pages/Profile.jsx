import React, { useState } from 'react'
import { useAuth } from '../hooks/useAuth'
import { changePassword, updateProfile } from '../services/api'

export default function Profile() {
  const { user, updateUserLocal } = useAuth()
  const [form, setForm] = useState({
    name: user?.name || '',
    phone: user?.phone || '',
    address: user?.address || '',
  })
  const [pwForm, setPwForm] = useState({ current_password: '', new_password: '', confirm: '' })
  const [msg, setMsg] = useState('')
  const [pwMsg, setPwMsg] = useState('')
  const [savingProfile, setSavingProfile] = useState(false)
  const [savingPw, setSavingPw] = useState(false)

  const handleProfileSubmit = async (e) => {
    e.preventDefault()
    setMsg('')
    setSavingProfile(true)
    try {
      const res = await updateProfile(form)
      updateUserLocal(res.data)
      setMsg('Profile updated successfully.')
    } catch (err) {
      setMsg(err.response?.data?.detail || 'Failed to update profile.')
    } finally {
      setSavingProfile(false)
    }
  }

  const handlePasswordSubmit = async (e) => {
    e.preventDefault()
    setPwMsg('')
    if (pwForm.new_password !== pwForm.confirm) {
      setPwMsg('New passwords do not match.')
      return
    }
    setSavingPw(true)
    try {
      await changePassword({
        current_password: pwForm.current_password,
        new_password: pwForm.new_password,
      })
      setPwMsg('Password changed successfully.')
      setPwForm({ current_password: '', new_password: '', confirm: '' })
    } catch (err) {
      setPwMsg(err.response?.data?.detail || 'Failed to change password.')
    } finally {
      setSavingPw(false)
    }
  }

  return (
    <div className="profile-page">
      <h1>My Profile</h1>

      <div className="profile-grid">
        <div className="card">
          <h3>Account Details</h3>
          {msg && <div className="alert-info">{msg}</div>}
          <form onSubmit={handleProfileSubmit} className="stacked-form">
            <label>
              Full name
              <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
            </label>
            <label>
              Email
              <input value={user?.email || ''} disabled />
            </label>
            <label>
              Phone
              <input value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} placeholder="+1 555 000 0000" />
            </label>
            <label>
              Shipping address
              <textarea value={form.address} onChange={(e) => setForm({ ...form, address: e.target.value })} rows={3} placeholder="Street, City, ZIP" />
            </label>
            <button className="btn-primary" disabled={savingProfile}>
              {savingProfile ? 'Saving…' : 'Save Changes'}
            </button>
          </form>
        </div>

        <div className="card">
          <h3>Change Password</h3>
          {pwMsg && <div className="alert-info">{pwMsg}</div>}
          <form onSubmit={handlePasswordSubmit} className="stacked-form">
            <label>
              Current password
              <input type="password" required value={pwForm.current_password}
                onChange={(e) => setPwForm({ ...pwForm, current_password: e.target.value })} />
            </label>
            <label>
              New password
              <input type="password" required minLength={6} value={pwForm.new_password}
                onChange={(e) => setPwForm({ ...pwForm, new_password: e.target.value })} />
            </label>
            <label>
              Confirm new password
              <input type="password" required value={pwForm.confirm}
                onChange={(e) => setPwForm({ ...pwForm, confirm: e.target.value })} />
            </label>
            <button className="btn-primary" disabled={savingPw}>
              {savingPw ? 'Updating…' : 'Update Password'}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}