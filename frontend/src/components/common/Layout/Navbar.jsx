import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../../hooks/useAuth'
import { Button } from '../UI/Button'

const Navbar = () => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="text-xl font-bold text-gray-900">
              CodeMaster
            </Link>
            <div className="hidden md:block ml-10">
              <div className="flex space-x-4">
                <Link 
                  to="/dashboard" 
                  className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md"
                >
                  Dashboard
                </Link>
                <Link 
                  to="/problems" 
                  className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md"
                >
                  Problems
                </Link>
                <Link 
                  to="/submissions" 
                  className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md"
                >
                  Submissions
                </Link>
              </div>
            </div>
          </div>
          <div className="flex items-center">
            {user ? (
              <>
                <span className="text-gray-700 mr-4">{user.username}</span>
                <Button variant="outline" onClick={handleLogout}>
                  Logout
                </Button>
              </>
            ) : (
              <>
                <Button variant="link" to="/login" className="mr-2">
                  Login
                </Button>
                <Button to="/register">Register</Button>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar;
