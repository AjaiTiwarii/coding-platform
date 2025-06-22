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
      console.log(`[${method.toUpperCase()}] ${url} →`, responseData)

      setData(responseData)
      return responseData
    } catch (err) {
      console.error(`API ${method.toUpperCase()} ${url} failed`, err)
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
