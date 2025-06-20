import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import { Alert } from '../common/UI/Alert'
import { Loader } from '../common/UI/Loader'
import { Input } from '../common/UI/Input'
import { Button } from '../common/UI/Button'
import { ErrorBoundary } from '../common/ErrorBoundary'

export const LoginForm = () => {
  const navigate = useNavigate()
  const { login, isAuthenticated } = useAuth()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  
  const { 
    register, 
    handleSubmit, 
    formState: { errors },
    reset 
  } = useForm()

  const onSubmit = async (data) => {
    try {
      setLoading(true)
      setError(null)
      
      const success = await login(data.email, data.password)
      
      if (success) {
        reset()
        navigate('/dashboard')
      } else {
        setError('Invalid email or password')
      }
    } catch (err) {
      setError(err.message || 'Login failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  // Redirect if already authenticated
  if (isAuthenticated) {
    navigate('/dashboard')
    return null
  }

  return (
    <ErrorBoundary>
      <div className="w-full max-w-md mx-auto">
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {error && (
          <Alert type="error" className="mb-4">
            {error}
          </Alert>
        )}
        
        <div className="space-y-4">
          <Input
            label="Email Address"
            type="email"
            placeholder="Enter your email"
            {...register('email', { 
              required: 'Email is required',
              pattern: {
                value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                message: 'Invalid email address'
              }
            })}
            error={errors.email?.message}
            disabled={loading}
          />
          
          <Input
            label="Password"
            type="password"
            placeholder="Enter your password"
            {...register('password', { 
              required: 'Password is required',
              minLength: {
                value: 6,
                message: 'Password must be at least 6 characters'
              }
            })}
            error={errors.password?.message}
            disabled={loading}
          />
        </div>
        
        <Button 
          type="submit" 
          className="w-full flex items-center justify-center py-3"
          disabled={loading}
          variant="primary"
        >
          {loading ? (
            <>
              <Loader size="sm" className="mr-2" />
              Signing In...
            </>
          ) : (
            'Sign In'
          )}
        </Button>
        
        <div className="text-center mt-4">
          <p className="text-sm text-gray-600">
            Don't have an account?{' '}
            <button
              type="button"
              onClick={() => navigate('/register')}
              className="text-primary-600 hover:text-primary-700 font-medium"
              disabled={loading}
            >
              Sign up here
            </button>
          </p>
        </div>
      </form>
    </div>
    </ErrorBoundary>
    
  )
}
