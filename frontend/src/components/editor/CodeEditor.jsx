// import { useRef, useState } from 'react'
// import Editor from '@monaco-editor/react'
// import { Button } from '../common/UI/Button'
// import { Loader } from '../common/UI/Loader'
// import { useApi } from '../../hooks/useApi'
// import { LanguageSelector } from './LanguageSelector'

// export const CodeEditor = ({ problemId }) => {
//   const editorRef = useRef(null)
//   const { post, loading } = useApi()
//   const [languageId, setLanguageId] = useState('')
//   const [output, setOutput] = useState(null)
//   const [error, setError] = useState(null)

//   const handleEditorDidMount = (editor) => {
//     editorRef.current = editor
//   }

//   const handleLanguageChange = (e) => {
//     setLanguageId(e.target.value)
//   }

//   const handleSubmit = async () => {
//     const code = editorRef.current?.getValue()
//     if (!code || !languageId) {
//       setError('Please select a language and write some code.')
//       return
//     }

//     setOutput(null)
//     setError(null)

//     try {
//       const response = await post('/submissions/submit/', {
//         code,
//         language: languageId,
//         problem: problemId,
//       })
//       setOutput(response.output || '✅ Submitted successfully!')
//     } catch (err) {
//       setError('❌ Submission failed. Please try again.')
//     }
//   }

//   return (
//     <div className="space-y-4">
//       {/* ✅ Language dropdown */}
//       {/* <LanguageSelector value={languageId} onChange={handleLanguageChange} /> */}

//       {/* ✅ Monaco Editor */}
//       <Editor
//         height="400px"
//         theme="vs-dark"
//         defaultLanguage="cpp"
//         defaultValue="// Start coding here"
//         onMount={handleEditorDidMount}
//       />

//       {/* ✅ Submit Button */}
//       {/* <div className="flex gap-4">
//         <Button onClick={handleSubmit} disabled={loading || !languageId}>
//           {loading ? <Loader size="sm" /> : 'Submit Code'}
//         </Button>
//       </div> */}

//       {/* ✅ Output/Error */}
//       {output && (
//         <div className="bg-gray-100 p-4 rounded">
//           <h4 className="font-semibold mb-2">Output:</h4>
//           <pre className="whitespace-pre-wrap text-sm">{output}</pre>
//         </div>
//       )}

//       {error && <div className="text-red-600">{error}</div>}
//     </div>
//   )
// }


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
