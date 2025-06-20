import { useState, useEffect } from 'react'
import { useLocalStorage } from './useLocalStorage'
import api from '../services/api'

// Utility functions for token management
export const getToken = () => {
  return localStorage.getItem('authToken')
}

// export const refreshToken = async () => {
//   try {
//     const response = await api.post('/auth/refresh/', { 
//       refresh: localStorage.getItem('refreshToken') 
//     })
//     const newAccessToken = response.data.access
//     localStorage.setItem('authToken', newAccessToken)
//     return newAccessToken
//   } catch (error) {
//     localStorage.removeItem('authToken')
//     localStorage.removeItem('refreshToken')
//     throw error
//   }
// }

// export const refreshToken = async () => {
//   const refresh = localStorage.getItem('refreshToken')
//   if (!refresh) {
//     throw new Error('No refresh token available')
//   }

//   try {
//     const response = await api.post('/auth/refresh/', {
//       refresh: refresh,
//     })

//     const newAccessToken = response.data.access
//     localStorage.setItem('authToken', newAccessToken)
//     return newAccessToken
//   } catch (error) {
//     console.error('🔁 Token refresh failed:', error.response?.data || error)
//     throw error
//   }
// }

export const refreshToken = async () => {
  const refresh = localStorage.getItem('refreshToken')
  if (!refresh) throw new Error('No refresh token found')

  try {
    const response = await api.post('/auth/token/refresh/', {
      refresh: refresh
    })

    const newAccessToken = response.data.access
    localStorage.setItem('authToken', newAccessToken)
    return newAccessToken
  } catch (error) {
    console.error('🔁 Refresh token failed:', error.response?.data || error)
    throw error
  }
}



// Main authentication hook
export const useAuth = () => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [token, setToken] = useLocalStorage('authToken', null)

  useEffect(() => {
    const loadUser = async () => {
      if (token) {
        try {
          const response = await api.get('/auth/profile/')
          setUser(response.data)
          setError(null)
        } catch (err) {
          console.error('Failed to load profile:', err)
          setToken(null)
          setUser(null)
          setError('Session expired. Please login again.')
        }
      }
      setLoading(false)
    }
    loadUser()
  }, [token])

  const login = async (email, password) => {
    try {
      const response = await api.post('/auth/login/', { email, password })
      setToken(response.data.tokens.access)
      localStorage.setItem('refreshToken', response.data.tokens.refresh)
      setUser(response.data.user)
      setError(null)  // ✅ clear previous error
      return true
    } catch (err) {
      console.error('Login failed:', err)
      setError(err.response?.data?.error || 'Login failed')
      return false
    }
  }

  const register = async (email, username, password) => {
    try {
      await api.post('/auth/register/', { email, username, password })
      setError(null)
      return true
    } catch (err) {
      setError(err.response?.data?.error || 'Registration failed')
      return false
    }
  }

  const logout = () => {
    setToken(null)
    setUser(null)
    setError(null)
    localStorage.removeItem('refreshToken')
    api.post('/auth/logout/').catch(() => {})  // ignore logout errors
  }

  return { 
    user, 
    loading, 
    error, 
    login, 
    register, 
    logout, 
    isAuthenticated: !!user 
  }
}
