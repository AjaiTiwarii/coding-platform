import { useState, useEffect } from 'react'

export const useLocalStorage = (key, initialValue) => {
  const readValue = () => {
    try {
      const item = window.localStorage.getItem(key)
      if (!item) return initialValue

      // 🔐 Try parsing only if it's valid JSON, else return raw string
      try {
        return JSON.parse(item)
      } catch {
        return item
      }
    } catch (error) {
      console.error(`❌ Error reading localStorage key "${key}":`, error)
      return initialValue
    }
  }

  const [storedValue, setStoredValue] = useState(readValue)

  const setValue = (value) => {
    try {
      const valueToStore = typeof value === 'object' ? JSON.stringify(value) : value
      window.localStorage.setItem(key, valueToStore)
      setStoredValue(value)
    } catch (error) {
      console.error(`❌ Error setting localStorage key "${key}":`, error)
    }
  }

  useEffect(() => {
    const handleStorageChange = (e) => {
      if (e.key === key) {
        try {
          const newValue = e.newValue
          setStoredValue(() => {
            try {
              return JSON.parse(newValue)
            } catch {
              return newValue
            }
          })
        } catch (error) {
          console.error(`❌ Error handling storage event for "${key}":`, error)
        }
      }
    }

    window.addEventListener('storage', handleStorageChange)
    return () => window.removeEventListener('storage', handleStorageChange)
  }, [key])

  return [storedValue, setValue]
}
