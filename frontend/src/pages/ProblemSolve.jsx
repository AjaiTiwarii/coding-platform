import { useParams } from 'react-router-dom'
import { ProblemDetail } from '../components/problems/ProblemDetail'
import { Layout } from '../components/common/Layout/Layout'
import { PrivateRoute } from '../components/auth/PrivateRoute'

export const ProblemSolvePage = () => {
  const { id } = useParams()

  return (
    <PrivateRoute>
      
        <ProblemDetail problemId={id} />
      
    </PrivateRoute>
  )
}
