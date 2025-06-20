// import { useEffect } from 'react'
// import { useApi } from '../../hooks/useApi'
// import { Statistics } from './Statistics'
// import { RecentActivity } from './RecentActivity'
// import { Alert } from '@/components/common/UI/Alert'
// import { Loader } from '@/components/common/UI/Loader'


// export const Dashboard = () => {
//   const { data: dashboardData, loading, error, get } = useApi()

//   useEffect(() => {
//     const fetchDashboardData = async () => {
//       // await get('/api/dashboard/')
//       await get('/auth/dashboard/')
//     }
//     fetchDashboardData()
//   }, [])

//   return (
//     <div className="p-6 space-y-8">
//       <h1 className="text-3xl font-bold text-gray-900">Dashboard Overview</h1>
      
//       {loading && <Loader />}
      
//       {error && (
//         <Alert type="error">Failed to load dashboard data: {error.message}</Alert>
//       )}

//       {!loading && !error && dashboardData && (
//         <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
//           <div className="lg:col-span-2">
//             <Statistics data={dashboardData} />
//           </div>
//           <div className="lg:col-span-1">
//             <RecentActivity activities={dashboardData.recent_activities} />
//           </div>
//         </div>
//       )}
//     </div>
//   )
// }


import { useEffect, useState } from 'react'
import { useApi } from '../../hooks/useApi'
import { Statistics } from './Statistics'
import { RecentActivity } from './RecentActivity'
import { Alert } from '@/components/common/UI/Alert'
import { Loader } from '@/components/common/UI/Loader'

export const Dashboard = () => {
  const { loading, error, get } = useApi()
  const [dashboardData, setDashboardData] = useState(null)

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const data = await get('/auth/dashboard/')
        setDashboardData(data)
      } catch (err) {
        console.error('❌ Failed to load dashboard data:', err)
      }
    }

    fetchDashboardData()
  }, [])

  return (
    <div className="p-6 space-y-8">
      <h1 className="text-3xl font-bold text-gray-900">Dashboard Overview</h1>
      
      {loading && <Loader />}

      {error && (
        <Alert type="error">Failed to load dashboard data: {error.message}</Alert>
      )}

      {!loading && !error && dashboardData && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <Statistics data={dashboardData} />
          </div>
          <div className="lg:col-span-1">
            <RecentActivity activities={dashboardData.recent_activities} />
          </div>
        </div>
      )}
    </div>
  )
}
