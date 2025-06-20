import { Link } from 'react-router-dom'
import clsx from 'clsx'

export const Button = ({ 
  children, 
  variant = 'primary', 
  to, 
  className, 
  ...props 
}) => {
  const baseStyles = 'inline-flex items-center px-4 py-2 rounded-md text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2'
  
  const variants = {
    primary: 'bg-primary-600 text-white hover:bg-primary-700',
    outline: 'border border-gray-300 text-gray-700 hover:bg-gray-50',
    link: 'text-primary-600 hover:text-primary-700 underline'
  }

  const Component = to ? Link : 'button'

  return (
    <Component
      className={clsx(baseStyles, variants[variant], className)}
      to={to}
      {...props}
    >
      {children}
    </Component>
  )
}
