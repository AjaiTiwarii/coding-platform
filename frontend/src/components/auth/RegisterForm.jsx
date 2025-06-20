import { useForm } from 'react-hook-form'
import { useAuth } from '../../hooks/useAuth'
import { Alert } from '../common/UI/Alert'
import { Loader } from '../common/UI/Loader'
import { Input } from '../common/UI/Input'
import { Button } from '../common/UI/Button'
import { useNavigate } from 'react-router-dom'

export const RegisterForm = () => {
  const navigate = useNavigate()
  const { register: signup, error, loading } = useAuth()

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors }
  } = useForm()

  const onSubmit = async (data) => {
    const success = await signup({
      email: data.email,
      username: data.username,
      password: data.password,
      password_confirm: data.confirmPassword,
      first_name: data.firstName,
      last_name: data.lastName,
      preferred_language: data.language || 'python'
    })
    if (success) {
      alert('Registration successful!')
      navigate('/dashboard')
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {error && (
        <Alert type="error">
          {typeof error === 'string'
            ? error
            : Object.entries(error).map(([field, msgs], i) =>
                Array.isArray(msgs)
                  ? msgs.map((msg, j) => (
                      <div key={`${field}-${j}`}>{`${field}: ${msg}`}</div>
                    ))
                  : <div key={i}>{`${field}: ${msgs}`}</div>
              )}
        </Alert>
      )}

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
        label="First Name"
        {...register('firstName', {
          required: 'First name is required'
        })}
        error={errors.firstName?.message}
      />

      <Input
        label="Last Name"
        {...register('lastName', {
          required: 'Last name is required'
        })}
        error={errors.lastName?.message}
      />

      <Input
        label="Preferred Language"
        defaultValue="python"
        {...register('language')}
        error={errors.language?.message}
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
