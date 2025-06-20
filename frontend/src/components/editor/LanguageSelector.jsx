// import { useEffect } from 'react'
// import { useApi } from '../../hooks/useApi'
// import { Select } from '../common/UI/Select'

// export const LanguageSelector = ({ value, onChange }) => {
//   const { data: languages, get } = useApi()

//   useEffect(() => {
//     // get('/api/submissions/languages/')
//     get('/submissions/languages/')
//   }, [])

//   const languageOptions = languages?.map(lang => ({
//     value: lang.id,
//     label: `${lang.name} (${lang.version})`
//   })) || []

//   return (
//     <Select
//       value={value}
//       onChange={onChange}
//       options={[
//         { value: '', label: 'Select Language' },
//         ...languageOptions
//       ]}
//       className="min-w-[200px]"
//     />
//   )
// }


import { useEffect, useState } from 'react'
import { useApi } from '../../hooks/useApi'

export const LanguageSelector = ({ value, onChange }) => {
  const { data, get } = useApi()
  const [languages, setLanguages] = useState([])

  useEffect(() => {
    const fetchLanguages = async () => {
      try {
        const response = await get('/submissions/languages/')
        // ✅ Make sure we extract correct array
        // if (Array.isArray(response)) {
        //   setLanguages(response)
        // } else if (Array.isArray(response.languages)) {
        //   setLanguages(response.languages)
        // } else {
        //   console.warn("⚠️ Unexpected response from languages API:", response)
        //   setLanguages([])
        // }
        // if (Array.isArray(response.languages)) {
        //   setLanguages(response.languages)
        // } else if (Array.isArray(response)) {
        //   setLanguages(response)
        // } else {
        //   console.warn("⚠️ Unexpected response from languages API:", response)
        //   setLanguages([])
        // }

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
