import { useEffect } from 'react'
import { useApi } from '../../hooks/useApi'
import { Loader } from '../common/UI/Loader'
import { Alert } from '../common/UI/Alert'

export const SubmissionHistory = () => {
  const { data, loading, error, get } = useApi()

  useEffect(() => {
    const fetchSubmissions = async () => {
      try {
        const result = await get('/submissions/history/')
        console.log("Submissions fetched:", result)
      } catch (err) {
        console.error('Failed to fetch submissions:', err)
      }
    }

    fetchSubmissions()
  }, [])

  const submissions = Array.isArray(data?.results) ? data.results : (Array.isArray(data) ? data : [])

  if (loading) return <Loader />
  if (error) return <Alert type="error">Failed to load submissions</Alert>

  if (submissions.length === 0) {
    return (
      <div className="text-center text-gray-600">
        You haven't submitted any solutions yet.
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {submissions.map(submission => (
        <div
          key={submission.id}
          className="bg-white rounded-lg shadow p-4"
        >
          <p><strong>Problem:</strong> {submission.problem_title}</p>
          <p><strong>Status:</strong> {submission.status}</p>
          <p><strong>Language:</strong> {submission.language_name}</p>
          <p><strong>Submitted:</strong> {new Date(submission.submitted_at || 'N/A').toLocaleString()}</p>
        </div>
      ))}
    </div>
  )
}
