// import axios from 'axios';
// import { getToken, refreshToken } from '../hooks/useAuth';

// const api = axios.create({
//   baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
//   timeout: 10000,
//   headers: {
//     'Content-Type': 'application/json',
//   },
// });

// // ✅ Request interceptor: Attach token except for /auth/refresh/
// api.interceptors.request.use(
//   (config) => {
//     const token = getToken();

//     if (token && !config.url.includes('/auth/refresh/')) {
//       config.headers.Authorization = `Bearer ${token}`;
//     }

//     return config;
//   },
//   (error) => Promise.reject(error)
// );

// // ✅ Response interceptor: Auto-refresh token on 401
// api.interceptors.response.use(
//   (response) => response,
//   async (error) => {
//     const originalRequest = error.config;

//     // If 401 and not already retried
//     if (error.response?.status === 401 && !originalRequest._retry) {
//       originalRequest._retry = true;

//       try {
//         const newToken = await refreshToken();
//         // Update token for retry
//         originalRequest.headers.Authorization = `Bearer ${newToken}`;
//         return api(originalRequest);
//       } catch (refreshError) {
//         // Optional: Clear tokens and force logout
//         localStorage.removeItem('authToken');
//         localStorage.removeItem('refreshToken');
//         console.error('Token refresh failed:', refreshError);
//         return Promise.reject(refreshError);
//       }
//     }

//     return Promise.reject(error);
//   }
// );

// export default api;


import axios from 'axios';
import { getToken, refreshToken } from '../hooks/useAuth';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ✅ Request interceptor: Attach token except for /auth/refresh/
api.interceptors.request.use(
  (config) => {
    let token = getToken();

    // Fallback to localStorage if getToken is undefined or broken
    if (!token) {
      token = localStorage.getItem('accessToken');
    }

    if (token && !config.url.includes('/auth/refresh/')) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// ✅ Response interceptor: Auto-refresh token on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const newToken = await refreshToken();

        if (newToken) {
          // Save to localStorage if not already
          localStorage.setItem('accessToken', newToken);
          originalRequest.headers.Authorization = `Bearer ${newToken}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Optional: Clear tokens and force logout
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        console.error('Token refresh failed:', refreshError);
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
