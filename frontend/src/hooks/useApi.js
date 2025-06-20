// import { useState } from 'react'
// import axios from 'axios'
// import { useLocalStorage } from './useLocalStorage'


// export const useApi = () => {
//   const [token] = useLocalStorage('authToken')
//   const [loading, setLoading] = useState(false)
//   const [error, setError] = useState(null)

//   const request = async (method, url, data = null, params = null) => {
//     setLoading(true)
//     try {
//       const response = await axios({
//         method,
//         url: process.env.VITE_API_BASE_URL + url,
//         headers: token ? { Authorization: `Bearer ${token}` } : {},
//         data,
//         params
//       })
//       return response.data
//     } catch (err) {
//       setError(err.response?.data || { message: 'API request failed' })
//       throw err
//     } finally {
//       setLoading(false)
//     }
//   }

//   return {
//     loading,
//     error,
//     get: (url, config) => request('get', url, null, config?.params),
//     post: (url, data) => request('post', url, data),
//     put: (url, data) => request('put', url, data),
//     delete: (url) => request('delete', url),
//   }
// }


// src/hooks/useApi.js
// import { useState } from 'react'
// import axios from 'axios'
// import { useLocalStorage } from './useLocalStorage'

// const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

// export const useApi = () => {
//   const [token] = useLocalStorage('authToken')
//   const [loading, setLoading] = useState(false)
//   const [error, setError] = useState(null)

//   const request = async (method, url, data = null, params = null) => {
//     setLoading(true)
//     try {
//       const response = await axios({
//         method,
//         url: `${baseUrl}${url}`,
//         headers: token ? { Authorization: `Bearer ${token}` } : {},
//         data,
//         params,
//       })
//       return response.data
//     } catch (err) {
//       setError(err.response?.data || { message: 'API request failed' })
//       throw err
//     } finally {
//       setLoading(false)
//     }
//   }

//   return {
//     loading,
//     error,
//     get: (url, config) => request('get', url, null, config?.params),
//     post: (url, data) => request('post', url, data),
//     put: (url, data) => request('put', url, data),
//     delete: (url) => request('delete', url),
//   }
// }


// src/hooks/useApi.js
// import { useState } from 'react'
// import api from '../services/api'

// export const useApi = () => {
//   const [loading, setLoading] = useState(false)
//   const [error, setError] = useState(null)

//   const [data, setData] = useState(null)

//   const request = async (method, url, data = null, params = null) => {
//     setLoading(true)
//     try {
//       const response = await api({
//         method,
//         url,
//         data,
//         params,
//       })
//       setData(response.data)
//       return response.data
//     } catch (err) {
//       setError(err.response?.data || { message: 'API request failed' })
//       throw err
//     } finally {
//       setLoading(false)
//     }
//   }

//   return {
//     data,
//     loading,
//     error,
//     get: (url, config) => request('get', url, null, config?.params),
//     post: (url, data) => request('post', url, data),
//     put: (url, data) => request('put', url, data),
//     delete: (url) => request('delete', url),
//   }
// }


import { useState } from 'react'
import api from '../services/api'

export const useApi = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [data, setData] = useState(null)

  const request = async (method, url, payload = null, params = null) => {
    setLoading(true)
    setError(null)

    try {
      const response = await api({
        method,
        url,
        data: payload,
        params,
      })

      const responseData = response.data

      // Debug log
      console.log(`✅ [${method.toUpperCase()}] ${url} →`, responseData)

      setData(responseData)
      return responseData
    } catch (err) {
      console.error(`❌ API ${method.toUpperCase()} ${url} failed`, err)
      setError(err.response?.data || { message: 'API request failed' })
      throw err
    } finally {
      setLoading(false)
    }
  }

  return {
    data,                          // raw data
    loading,
    error,
    list: Array.isArray(data?.results) ? data.results : (Array.isArray(data) ? data : []), // safe list
    get: (url, config) => request('get', url, null, config?.params),
    post: (url, payload) => request('post', url, payload),
    put: (url, payload) => request('put', url, payload),
    delete: (url) => request('delete', url),
  }
}
