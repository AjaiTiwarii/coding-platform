import { useForm } from 'react-hook-form'
import { useAuth } from '../../hooks/useAuth'
import { Alert } from '../common/UI/Alert'
import { Loader } from '../common/UI/Loader'
import { Input } from '../common/UI/Input'
import { Button } from '../common/UI/Button'

export const RegisterForm = () => {
  const { register: signup, error, loading } = useAuth()
  const { 
    register, 
    handleSubmit, 
    watch,
    formState: { errors } 
  } = useForm()

  const onSubmit = async (data) => {
    await signup(data.email, data.username, data.password)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {error && <Alert type="error">{error}</Alert>}
      
      <Input
        label="Email"
        type="email"
        {...register('email', { 
          required: 'Email is required',
          pattern: {
            value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
            message: 'Invalid email address'
          }
        })}
        error={errors.email?.message}
      />
      
      <Input
        label="Username"
        {...register('username', { 
          required: 'Username is required',
          minLength: {
            value: 3,
            message: 'Username must be at least 3 characters'
          }
        })}
        error={errors.username?.message}
      />
      
      <Input
        label="Password"
        type="password"
        {...register('password', { 
          required: 'Password is required',
          minLength: {
            value: 8,
            message: 'Password must be at least 8 characters'
          }
        })}
        error={errors.password?.message}
      />
      
      <Input
        label="Confirm Password"
        type="password"
        {...register('confirmPassword', {
          validate: value => 
            value === watch('password') || 'Passwords do not match'
        })}
        error={errors.confirmPassword?.message}
      />
      
      <Button type="submit" className="w-full" disabled={loading}>
        {loading ? <Loader size="sm" /> : 'Create Account'}
      </Button>
    </form>
  )
}
