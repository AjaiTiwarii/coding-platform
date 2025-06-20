// import { useEffect, useState, useRef } from 'react'
// import { useParams, useNavigate } from 'react-router-dom'
// import { useApi } from '../../hooks/useApi'
// import { Loader } from '../common/UI/Loader'
// import { Alert } from '../common/UI/Alert'
// import { CodeEditor } from '../editor/CodeEditor'
// import { LanguageSelector } from '../editor/LanguageSelector'
// import { Button } from '../common/UI/Button'

// export const ProblemDetail = () => {
//   const { id: problemId } = useParams()
//   const navigate = useNavigate()
//   const { data: problem, loading, error, get, post } = useApi()

//   const [languageId, setLanguageId] = useState(null)
//   const [submitting, setSubmitting] = useState(false)
//   const editorRef = useRef(null)

//   useEffect(() => {
//     const fetchProblem = async () => {
//       try {
//         await get(`/problems/problems/${problemId}/`)
//       } catch (err) {
//         console.error('Failed to fetch problem:', err)
//       }
//     }
//     fetchProblem()
//   }, [problemId])

//   const handleEditorMount = (editor) => {
//     editorRef.current = editor
//   }

//   const handleSubmit = async () => {
//     const code = editorRef.current?.getValue()

//     if (!languageId || !code?.trim()) {
//       alert('Please select a language and enter some code before submitting.')
//       return
//     }

//     setSubmitting(true)
//     try {
//       // await post('/submissions/', {
//       //   problem: problemId,
//       //   language: languageId,
//       //   code,
//       // })
//       await post('/submissions/submit/', {
//         problem: problemId,
//         language: languageId,
//         code,
//       })
//       alert('✅ Code submitted successfully! Redirecting...')
//       navigate('/submissions')
//     } catch (err) {
//       console.error('❌ Submission failed:', err)
//       alert('Failed to submit code. Please try again.')
//     } finally {
//       setSubmitting(false)
//     }
//   }

//   if (loading) return <Loader />
//   if (error) return <Alert type="error">{error.message}</Alert>

//   return (
//     <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 p-4">
//       <div className="space-y-6">
//         <h1 className="text-2xl font-bold">{problem?.title}</h1>
//         <div className="prose max-w-none" dangerouslySetInnerHTML={{ __html: problem?.description }} />
//         <div className="space-y-4">
//           <h3 className="font-medium">Sample Input</h3>
//           <pre className="bg-gray-50 p-4 rounded-md">{problem?.sample_input}</pre>
//           <h3 className="font-medium">Sample Output</h3>
//           <pre className="bg-gray-50 p-4 rounded-md">{problem?.sample_output}</pre>
//         </div>
//       </div>

//       <div className="space-y-6">
//         <LanguageSelector value={languageId} onChange={setLanguageId} />
//         <CodeEditor onMount={handleEditorMount} />
//         <Button
//           type="button"
//           className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-md"
//           onClick={handleSubmit}
//           disabled={submitting || !languageId}
//         >
//           {submitting ? 'Submitting...' : 'Submit Code'}
//         </Button>
//       </div>
//     </div>
//   )
// }


import { useEffect, useState, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useApi } from '../../hooks/useApi'
import { Loader } from '../common/UI/Loader'
import { Alert } from '../common/UI/Alert'
import { CodeEditor } from '../editor/CodeEditor'
import { LanguageSelector } from '../editor/LanguageSelector'
import { Button } from '../common/UI/Button'

export const ProblemDetail = () => {
  const { id: problemId } = useParams()
  const navigate = useNavigate()
  const { data: problem, loading, error, get, post } = useApi()

  const [languageId, setLanguageId] = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const [submitError, setSubmitError] = useState(null)
  const [output, setOutput] = useState(null)

  const editorRef = useRef(null)

  useEffect(() => {
    const fetchProblem = async () => {
      try {
        await get(`/problems/problems/${problemId}/`)
      } catch (err) {
        console.error('Failed to fetch problem:', err)
      }
    }
    fetchProblem()
  }, [problemId])

  const handleEditorMount = (editor) => {
    editorRef.current = editor
  }

  const handleSubmit = async () => {
    const code = editorRef.current?.getValue()

    console.log("▶️ Submitted Code:", code); 

    setSubmitError(null)
    setOutput(null)

    if (!languageId || !code?.trim()) {
      setSubmitError('⚠️ Please select a language and write some code.')
      return
    }

    setSubmitting(true)

    try {
      const response = await post('/submissions/submit/', {
        code,
        language: languageId,
        problem: problemId,
      })

      setOutput(response.output || '✅ Submitted successfully!')
      // Optional: Redirect after a delay
      setTimeout(() => navigate('/submissions'), 2000)
    } catch (err) {
        console.error('❌ Submission failed:', err)

        const message =
          err.response?.data?.error ||
          err.response?.data?.message ||
          'Failed to submit code. Please try again.'

        setSubmitError(message)
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) return <Loader />
  if (error) return <Alert type="error">{error.message}</Alert>

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 p-4">
      {/* LEFT: Problem Description */}
      <div className="space-y-6">
        <h1 className="text-2xl font-bold">{problem?.title}</h1>

        <div className="prose max-w-none" dangerouslySetInnerHTML={{ __html: problem?.description }} />

        <div className="space-y-4">
          <h3 className="font-medium">Sample Input</h3>
          <pre className="bg-gray-50 p-4 rounded-md">{problem?.sample_input}</pre>

          <h3 className="font-medium">Sample Output</h3>
          <pre className="bg-gray-50 p-4 rounded-md">{problem?.sample_output}</pre>
        </div>
      </div>

      {/* RIGHT: Code Editor */}
      <div className="space-y-6">
        <LanguageSelector value={languageId} onChange={setLanguageId} />
        <CodeEditor onMount={handleEditorMount} />

        <Button
          type="button"
          className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-md"
          onClick={handleSubmit}
          disabled={submitting || !languageId}
        >
          {submitting ? 'Submitting...' : 'Submit Code'}
        </Button>

        {submitError && <Alert type="error">{submitError}</Alert>}
        {output && (
          <div className="bg-gray-100 p-4 rounded">
            <h4 className="font-semibold mb-2">Output:</h4>
            <pre className="whitespace-pre-wrap text-sm">{output}</pre>
          </div>
        )}
      </div>
    </div>
  )
}
