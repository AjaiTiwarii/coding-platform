import { SubmissionHistory } from '../components/submissions/SubmissionHistory'
import { Layout } from '../components/common/Layout/Layout'
import { PrivateRoute } from '../components/auth/PrivateRoute'

export const SubmissionsPage = () => {
  return (
    <PrivateRoute>
      
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold mb-8">Submission History</h1>
          <SubmissionHistory />
        </div>

    </PrivateRoute>
  )
}
