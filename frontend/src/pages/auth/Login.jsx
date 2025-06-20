import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import { LoginForm } from '../../components/auth/LoginForm'
import { Layout } from '../../components/common/Layout/Layout'


export const LoginPage = () => {
  const { user } = useAuth()
  const navigate = useNavigate()


  console.log("🔁 Rendering LoginPage, user =", user)

  return (
    <div className="max-w-md mx-auto py-12">
      <h1 className="text-3xl font-bold text-center mb-8">Sign In to CodeMaster</h1>
      <LoginForm />
    </div>
  )
}
