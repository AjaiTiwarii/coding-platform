import { Link } from 'react-router-dom'
import { getDifficultyColor } from '../../utils/helpers'

export const ProblemCard = ({ problem }) => {
  const difficultyColor = getDifficultyColor(problem.difficulty)

  return (
    <div className="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-medium">
          <Link 
            to={`/problems/${problem.id}`}
            className="text-gray-900 hover:text-primary-600"
          >
            {problem.title}
          </Link>
        </h3>
        <span className={`px-2 py-1 text-xs font-medium rounded-full ${difficultyColor}`}>
          {problem.difficulty}
        </span>
      </div>
      
      <div className="text-sm text-gray-600 mb-4 line-clamp-3">
        {problem.description}
      </div>

      <div className="flex items-center justify-between text-sm">
        <div className="text-gray-500">
          Acceptance: {problem.success_rate || 0}%
        </div>
        <div className="flex space-x-2">
          {problem.tags?.map(tag => (
            <span 
              key={tag.id}
              className="px-2 py-1 bg-gray-100 text-gray-700 rounded-full text-xs"
            >
              {tag.name}
            </span>
          ))}
        </div>
      </div>
    </div>
  )
}
