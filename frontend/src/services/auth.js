import api from './api';

export const authService = {
  login: async (email, password) => {
    try {
      const response = await api.post('/auth/login/', { email, password });
      return {
        success: true,
        data: response.data,
        tokens: response.data.tokens
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Login failed'
      };
    }
  },

  register: async (userData) => {
    try {
      const response = await api.post('/auth/register/', userData);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Registration failed'
      };
    }
  },

  getProfile: async () => {
    try {
      const response = await api.get('/auth/profile/');
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to load profile'
      };
    }
  },

  logout: async () => {
    try {
      await api.post('/auth/logout/');
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Logout failed'
      };
    }
  }
};
