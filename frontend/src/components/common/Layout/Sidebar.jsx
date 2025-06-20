import { Link } from 'react-router-dom'
// import { useAuth } from '../../hooks/useAuth'
import { useAuth } from '../../../hooks/useAuth'

const Sidebar = () => {
  const { user } = useAuth()

  return (
    <div className="w-64 bg-white border-r border-gray-200 p-4">
      <div className="mb-6">
        {user && (
          <div className="p-4 bg-gray-50 rounded-lg">
            <h3 className="text-sm font-medium text-gray-900">{user.username}</h3>
            <p className="text-xs text-gray-600 mt-1">Rating: {user.rating || 0}</p>
          </div>
        )}
      </div>
      <nav className="space-y-1">
        <Link 
          to="/dashboard" 
          className="flex items-center p-2 text-gray-700 hover:bg-gray-100 rounded-md"
        >
          Dashboard
        </Link>
        <Link 
          to="/problems" 
          className="flex items-center p-2 text-gray-700 hover:bg-gray-100 rounded-md"
        >
          Problems
        </Link>
        <Link 
          to="/submissions" 
          className="flex items-center p-2 text-gray-700 hover:bg-gray-100 rounded-md"
        >
          Submissions
        </Link>
        <Link 
          to="/profile" 
          className="flex items-center p-2 text-gray-700 hover:bg-gray-100 rounded-md"
        >
          Profile
        </Link>
      </nav>
    </div>
  )
}

export default Sidebar;
