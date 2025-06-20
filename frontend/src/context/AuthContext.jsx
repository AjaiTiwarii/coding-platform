import { createContext, useContext, useState, useEffect } from 'react'
import { useLocalStorage } from '../hooks/useLocalStorage'
import api from '../services/api'

const AuthContext = createContext()

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [token, setToken] = useLocalStorage('authToken', null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadUser = async () => {
      if (token) {
        try {
          const response = await api.get('/auth/profile/')
          setUser(response.data)
        } catch (error) {
          setToken(null)
        }
      }
      setLoading(false)
    }
    loadUser()
  }, [token])

  const login = async (email, password) => {
    try {
      const response = await api.post('/auth/login/', { email, password })
      setToken(response.data.access)
      setUser(response.data.user)
      return true
    } catch (error) {
      return false
    }
  }

  const logout = () => {
    setToken(null)
    setUser(null)
    api.post('/auth/logout/')
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  return useContext(AuthContext)
}
