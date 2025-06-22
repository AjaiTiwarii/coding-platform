import { useState, useEffect } from 'react'
import { useLocalStorage } from './useLocalStorage'
import api from '../services/api'

// Utility: get token
export const getToken = () => {
  return localStorage.getItem('authToken')
}

// Utility: refresh token
export const refreshToken = async () => {
  const refresh = localStorage.getItem('refreshToken');
  if (!refresh) throw new Error('No refresh token found');

  try {
    const response = await api.post('/auth/token/refresh/', { refresh });
    const newAccessToken = response.data.access;
    localStorage.setItem('authToken', newAccessToken);
    return newAccessToken;
  } catch (error) {
    console.error('Refresh token failed:', error.response?.data || error);
    throw error;
  }
};

// Main hook
export const useAuth = () => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [token, setToken] = useLocalStorage('authToken', null)

  useEffect(() => {
    const loadUser = async () => {
      if (token) {
        try {
          const response = await api.get('/auth/profile/');
          setUser(response.data);
          setError(null);
        } catch (err) {
          console.error('Failed to load profile:', err);
          setToken(null);
          setUser(null);
          setError('Session expired. Please login again.');
        }
      }
      setLoading(false);
    }

    loadUser();
  }, [token]);

  const login = async (email, password) => {
    try {
      const response = await api.post('/auth/login/', { email, password });

      setToken(response.data.tokens.access);
      localStorage.setItem('refreshToken', response.data.tokens.refresh);
      setUser(response.data.user);
      setError(null);
      return true;
    } catch (err) {
      console.error('Login failed:', err);
      setError(err.response?.data?.error || 'Login failed');
      return false;
    }
  }



  const register = async (userData) => {
    try {
      await api.post('/auth/register/', userData);
      setError(null);
      return true;
    } catch (err) {
      const errData = err.response?.data;
      setError(errData || 'Registration failed');

      return false;
    }
  };


  const logout = () => {
    setToken(null);
    setUser(null);
    setError(null);
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('authToken');
    api.post('/auth/logout/').catch(() => {});
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
