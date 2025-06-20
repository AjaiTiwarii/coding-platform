import Editor from '@monaco-editor/react'

export const CodeEditor = ({ onMount }) => {
  return (
    <Editor
      height="400px"
      theme="vs-dark"
      defaultLanguage="cpp"
      defaultValue="// Start coding here"
      onMount={onMount}
    />
  )
}
