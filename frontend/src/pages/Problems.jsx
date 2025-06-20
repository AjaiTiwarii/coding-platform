import { ProblemList } from '../components/problems/ProblemList'
import { Layout } from '../components/common/Layout/Layout'
import { PrivateRoute } from '../components/auth/PrivateRoute'

export const ProblemsPage = () => {
  return (
    <PrivateRoute>
      
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold mb-8">Coding Problems</h1>
          <ProblemList />
        </div>
      
    </PrivateRoute>
  )
}
