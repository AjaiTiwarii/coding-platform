import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import { RegisterForm } from '../../components/auth/RegisterForm'
import { Layout } from '../../components/common/Layout/Layout'

export const RegisterPage = () => {
  const { user } = useAuth()
  const navigate = useNavigate()

  if (user) {
    navigate('/dashboard')
  }

  return (
    
      <div className="max-w-md mx-auto py-12">
        <h1 className="text-3xl font-bold text-center mb-8">Create New Account</h1>
        <RegisterForm />
      </div>
    
  )
}
