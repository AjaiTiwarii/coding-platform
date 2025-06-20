import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useApi } from '../../hooks/useApi'
import { Loader } from '../common/UI/Loader'
import { Alert } from '../common/UI/Alert'
import { Progress } from '../common/UI/Progress'

export const SubmissionStatus = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const { data: submission, get } = useApi()
  const [pollingCount, setPollingCount] = useState(0)

  useEffect(() => {
    const interval = setInterval(async () => {
      await get(`/submissions/${id}/`)
      setPollingCount(prev => prev + 1)
    }, 2000)

    return () => clearInterval(interval)
  }, [id])

  useEffect(() => {
    if (submission?.status && !['PENDING', 'RUNNING'].includes(submission.status)) {
      navigate(`/submissions/${id}/result`)
    }
  }, [submission?.status])

  const getStatusMessage = () => {
    switch(submission?.status) {
      case 'PENDING': return 'Waiting in queue...'
      case 'RUNNING': return 'Executing your code...'
      default: return 'Processing results...'
    }
  }

  return (
    <div className="max-w-2xl mx-auto py-12 text-center">
      <Loader size="lg" />
      <h2 className="mt-4 text-xl font-medium text-gray-900">
        {getStatusMessage()}
      </h2>
      <div className="mt-6">
        <Progress 
          value={pollingCount * 10} 
          max={100} 
          className="h-2 bg-gray-200"
        />
      </div>
      <p className="mt-4 text-sm text-gray-600">
        This usually takes 10-30 seconds. Please don't close this page.
      </p>
    </div>
  )
}
