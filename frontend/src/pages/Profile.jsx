import { useAuth } from '../hooks/useAuth'
import { Layout } from '../components/common/Layout/Layout'
import { PrivateRoute } from '../components/auth/PrivateRoute'

export const ProfilePage = () => {
  const { user } = useAuth()

  return (
    <PrivateRoute>
        <div className="max-w-3xl mx-auto py-8">
          <h1 className="text-3xl font-bold mb-8">Profile Settings</h1>
          <div className="bg-white p-6 rounded-lg shadow-sm">
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Username</label>
                <p className="mt-1 text-gray-900">{user?.username}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Email</label>
                <p className="mt-1 text-gray-900">{user?.email}</p>
              </div>
            </div>
          </div>
        </div>
    </PrivateRoute>
  )
}
