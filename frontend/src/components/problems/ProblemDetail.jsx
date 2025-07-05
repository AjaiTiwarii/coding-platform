import { get, post } from '../../services/api'
import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { CodeEditor } from '../editor/CodeEditor'
import { Button } from '../common/UI/Button'

export const ProblemDetail = () => {
  const { id: problemId } = useParams()
  const [problem, setProblem] = useState(null)
  const [languages, setLanguages] = useState([])
  const [languageId, setLanguageId] = useState(null)
  const [code, setCode] = useState('')
  const [loading, setLoading] = useState(false)
  const [submissionResult, setSubmissionResult] = useState(null)
  const [submitError, setSubmitError] = useState(null)

  // Fetch problem
  useEffect(() => {
    const fetchProblem = async () => {
      try {
        const response = await get(`/problems/problems/${problemId}/`)
        setProblem(response)
        setCode(response?.starter_code || '')
      } catch (err) {
        console.error('[fetchProblem] Error:', err)
      }
    }
    fetchProblem()
  }, [problemId])

  // Fetch languages
  useEffect(() => {
    const fetchLanguages = async () => {
      try {
        const response = await get('/submissions/languages/')
        if (Array.isArray(response.results)) {
          setLanguages(response.results)
          setLanguageId(response.results[0]?.id || null)
        } else {
          console.warn('⚠ Unexpected languages format:', response)
        }
      } catch (err) {
        console.error('Failed to fetch languages:', err)
      }
    }
    fetchLanguages()
  }, [])

  const selectedLanguage = languages.find((lang) => lang.id === languageId)
  const selectedLanguageName = selectedLanguage?.name?.toLowerCase() || 'python'

  const handleSubmit = async () => {
    setLoading(true)
    setSubmitError(null)
    setSubmissionResult(null)

    if (!problem || !problem.id || !languageId || !code.trim()) {
      setSubmitError('Please ensure code, problem, and language are all set.')
      setLoading(false)
      return
    }

    if (selectedLanguageName === 'python' && code.includes('//')) {
      setSubmitError("Invalid syntax: Use '#' instead of '//' for comments in Python.")
      setLoading(false)
      return
    }

    try {
      const payload = {
        code,
        language: languageId,
        problem: problem.id,
      }

      const response = await post('/submissions/submit/', payload)
      const submissionId = response.id
      setSubmissionResult({ status: 'PENDING', id: submissionId })

      const interval = setInterval(async () => {
        const result = await get(`/submissions/${submissionId}/`)
        if (result.status !== 'PENDING' && result.status !== 'RUNNING') {
          setSubmissionResult(result)
          clearInterval(interval)
          setLoading(false)
        }
      }, 2000)
    } catch (err) {
      const details = err.response?.data
      console.error('[handleSubmit] Submission error:', err)
      alert(
        details?.error ||
        details?.message ||
        'Something went wrong. Check the console for details.'
      )
      setLoading(false)
    }
  }

  if (!problem) return <div className="p-4 text-gray-600">Loading problem...</div>

  return (
    <div className="max-w-7xl mx-auto px-4 py-6">
      <div className="flex flex-col lg:flex-row gap-8">
        {/* Left Panel */}
        <div className="flex-1">
          <h1 className="text-2xl font-bold mb-4">{problem.title}</h1>
          <p className="mb-4 whitespace-pre-line">{problem.description}</p>

          {problem.sample_input && (
            <div className="mb-3">
              <h3 className="font-semibold">📥 Sample Input:</h3>
              <pre className="bg-gray-100 p-2 rounded">{problem.sample_input}</pre>
            </div>
          )}

          {problem.sample_output && (
            <div className="mb-3">
              <h3 className="font-semibold">📤 Sample Output:</h3>
              <pre className="bg-gray-100 p-2 rounded">{problem.sample_output}</pre>
            </div>
          )}
        </div>

        {/* Right Panel */}
        <div className="flex-1">
          <div className="mb-4">
            <label className="block mb-1 font-medium">Select Language:</label>
            <select
              value={languageId || ''}
              onChange={(e) => setLanguageId(Number(e.target.value))}
              className="border px-2 py-1 rounded w-full"
            >
              <option value="">Select Language</option>
              {languages.map((lang) => (
                <option key={lang.id} value={lang.id}>
                  {lang.name}
                </option>
              ))}
            </select>
          </div>

          <CodeEditor
            code={code}
            onChange={setCode}
            language={selectedLanguageName}
            placeholder={
              selectedLanguageName === 'python'
                ? '# Start coding here'
                : '// Start coding here'
            }
          />

          <Button onClick={handleSubmit} disabled={loading} className="mt-4 w-full">
            {loading ? 'Submitting...' : 'Submit Code'}
          </Button>

          {submitError && <div className="text-red-600 mt-2">{submitError}</div>}

          {submissionResult && (
            <div className="bg-gray-100 p-4 mt-6 rounded space-y-2">
              <h4 className="font-semibold mb-2">
                Verdict: <span className="text-blue-600">{submissionResult.status}</span>
              </h4>

              {(submissionResult.status === 'PENDING' || submissionResult.status === 'RUNNING') ? (
                <p className="text-sm text-gray-600 animate-pulse">⏳ Evaluating...</p>
              ) : (
                <>
                  {Array.isArray(submissionResult.test_results)
                    ? submissionResult.test_results.map((test, idx) => (
                        <div key={test.id || idx} className="border-t pt-2 text-sm">
                          <p><strong>Test Case {idx + 1}</strong></p>
                          <p>Status: <span className="font-mono">{test.status}</span></p>
                          <p>Output: <code>{test.output}</code></p>
                          {test.error_message && (
                            <p className="text-red-500">Error: <code>{test.error_message}</code></p>
                          )}
                          <p>Time: {test.execution_time} ms</p>
                        </div>
                      ))
                    : <p className="text-red-600">⚠ No test_results found.</p>}
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
