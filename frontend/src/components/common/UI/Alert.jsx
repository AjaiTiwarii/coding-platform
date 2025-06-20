export const Alert = ({ type = 'info', children }) => {
  const variants = {
    info: 'bg-blue-50 text-blue-700',
    success: 'bg-green-50 text-green-700',
    warning: 'bg-yellow-50 text-yellow-700',
    error: 'bg-red-50 text-red-700'
  }

  return (
    <div className={`p-4 rounded-md ${variants[type]}`}>
      <div className="flex items-center">
        <span className="flex-shrink-0">
          {/* Add appropriate icons here */}
        </span>
        <div className="ml-3">
          {children}
        </div>
      </div>
    </div>
  )
}
