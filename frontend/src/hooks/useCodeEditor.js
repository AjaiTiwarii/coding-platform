import { useState, useEffect } from 'react'
import { useLocalStorage } from './useLocalStorage'

export const useCodeEditor = (problemId) => {
  const [code, setCode] = useLocalStorage(`code-${problemId}`, '')
  const [language, setLanguage] = useLocalStorage('preferredLanguage', 'python')
  const [theme, setTheme] = useLocalStorage('editorTheme', 'vs-dark')
  const [fontSize, setFontSize] = useLocalStorage('editorFontSize', 14)
  const [tabSize, setTabSize] = useLocalStorage('editorTabSize', 2)

  const resetCode = () => {
    setCode('')
    localStorage.removeItem(`code-${problemId}`)
  }

  return {
    code,
    language,
    theme,
    fontSize,
    tabSize,
    setCode,
    setLanguage,
    setTheme,
    setFontSize: (size) => setFontSize(Number(size)),
    setTabSize: (size) => setTabSize(Number(size)),
    resetCode
  }
}
