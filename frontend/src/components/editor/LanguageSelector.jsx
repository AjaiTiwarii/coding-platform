import { useEffect, useState } from 'react'
import { useApi } from '../../hooks/useApi'

export const LanguageSelector = ({ value, onChange }) => {
  const { data, get } = useApi()
  const [languages, setLanguages] = useState([])

  useEffect(() => {
    const fetchLanguages = async () => {
      try {
        const response = await get('/submissions/languages/')

        if (Array.isArray(response.results)) {
          setLanguages(response.results)
        } else {
          console.warn("⚠️ Unexpected response from languages API:", response)
          setLanguages([])
        }


      } catch (err) {
        console.error('Failed to load languages:', err)
        setLanguages([])
      }
    }
    fetchLanguages()
  }, [])

  return (
    <select
      className="w-full border p-2 rounded"
      value={value || ''}
      onChange={(e) => onChange(Number(e.target.value))}
    >
      <option value="">Select Language</option>
      {languages.map(lang => (
        <option key={lang.id} value={lang.id}>
          {lang.name}
        </option>
      ))}
    </select>
  )
}
