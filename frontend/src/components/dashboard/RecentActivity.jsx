// import { formatDateTime } from '../utils/helpers'
// import { getStatusColor } from '../utils/helpers'
import { formatDateTime, getStatusColor } from '../../utils/helpers'

export const RecentActivity = ({ activities }) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-sm">
      <h2 className="text-xl font-semibold mb-4">Recent Activity</h2>
      <div className="space-y-4">
        {activities?.map(activity => (
          <div 
            key={activity.id}
            className="flex items-center justify-between p-4 bg-gray-50 rounded-md"
          >
            <div>
              <h3 className="font-medium">{activity.problem_title}</h3>
              <p className="text-sm text-gray-600">
                {formatDateTime(activity.timestamp)}
              </p>
            </div>
            <span className={`px-2 py-1 text-xs rounded-full ${getStatusColor(activity.status)}`}>
              {activity.status}
            </span>
          </div>
        ))}
        
        {activities?.length === 0 && (
          <div className="text-center text-gray-500 py-4">
            No recent activity
          </div>
        )}
      </div>
    </div>
  )
}
