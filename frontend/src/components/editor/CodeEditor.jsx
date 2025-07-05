
import Editor from '@monaco-editor/react'

export const CodeEditor = ({ code, onChange, language, placeholder }) => {
  return (
    <Editor
      height="400px"
      theme="vs-dark"
      language={language || 'python'}
      value={code}
      onChange={(value) => onChange(value)}
      options={{
        fontSize: 14,
        minimap: { enabled: false },
        scrollBeyondLastLine: false,
        wordWrap: 'on',
        placeholder: placeholder || '',
      }}
    />
  )
}
