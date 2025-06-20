export const getDifficultyColor = (difficulty) => {
  switch (difficulty?.toUpperCase()) {
    case 'EASY': return 'bg-green-100 text-green-800'
    case 'MEDIUM': return 'bg-yellow-100 text-yellow-800'
    case 'HARD': return 'bg-red-100 text-red-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}

export const getStatusColor = (status) => {
  switch (status?.toUpperCase()) {
    case 'ACCEPTED': return 'bg-green-100 text-green-800'
    case 'WRONG_ANSWER': return 'bg-red-100 text-red-800'
    case 'PENDING': return 'bg-yellow-100 text-yellow-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}

export const formatDateTime = (isoString) => {
  return new Date(isoString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

export const formatExecutionTime = (ms) => {
  return ms < 1000 ? `${ms}ms` : `${(ms / 1000).toFixed(2)}s`
}

export const calculateSuccessRate = (total, accepted) => {
  return total > 0 ? Math.round((accepted / total) * 100) : 0
}

export const truncateText = (text, maxLength = 100) => {
  return text.length > maxLength 
    ? text.substring(0, maxLength) + '...' 
    : text
}
