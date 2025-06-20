import { Dashboard } from '../components/dashboard/Dashboard'
import { Layout } from '../components/common/Layout/Layout'
import { PrivateRoute } from '../components/auth/PrivateRoute'

export const DashboardPage = () => {
  return (
    <PrivateRoute>
      
        <Dashboard />
      
    </PrivateRoute>
  )
}
