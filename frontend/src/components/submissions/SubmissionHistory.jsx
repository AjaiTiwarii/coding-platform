// import { useSearchParams } from 'react-router-dom'
// import { useApi } from '../../hooks/useApi'
// import { Loader } from '../common/UI/Loader'
// import { Alert } from '../common/UI/Alert'
// import { Pagination } from '../common/UI/Pagination'
// import { getStatusColor } from '../../utils/helpers'

// export const SubmissionHistory = () => {
//   const [searchParams] = useSearchParams()
//   const { data, loading, error, get } = useApi()

//   useEffect(() => {
//     const fetchSubmissions = async () => {
//       const params = Object.fromEntries(searchParams.entries())
//       // await get('/api/submissions/', { params })
//       await get('/submissions/', { params })
//     }
//     fetchSubmissions()
//   }, [searchParams])

//   return (
//     <div className="space-y-4">
//       {loading && <Loader />}
      
//       {error && (
//         <Alert type="error">Failed to load submissions: {error.message}</Alert>
//       )}

//       {!loading && !error && (
//         <>
//           <div className="bg-white rounded-lg shadow-sm overflow-hidden">
//             <table className="min-w-full divide-y divide-gray-200">
//               <thead className="bg-gray-50">
//                 <tr>
//                   <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Problem</th>
//                   <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Language</th>
//                   <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
//                   <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Time</th>
//                 </tr>
//               </thead>
//               <tbody className="bg-white divide-y divide-gray-200">
//                 {data?.results?.map(submission => (
//                   <tr key={submission.id}>
//                     <td className="px-6 py-4 whitespace-nowrap">
//                       <a 
//                         href={`/problems/${submission.problem.id}`}
//                         className="text-primary-600 hover:text-primary-700"
//                       >
//                         {submission.problem.title}
//                       </a>
//                     </td>
//                     <td className="px-6 py-4 whitespace-nowrap">
//                       {submission.language.name}
//                     </td>
//                     <td className="px-6 py-4 whitespace-nowrap">
//                       <span className={`px-2 py-1 text-xs rounded-full ${getStatusColor(submission.status)}`}>
//                         {submission.status}
//                       </span>
//                     </td>
//                     <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
//                       {new Date(submission.submitted_at).toLocaleString()}
//                     </td>
//                   </tr>
//                 ))}
//               </tbody>
//             </table>
//           </div>
          
//           <Pagination 
//             currentPage={data?.current_page || 1}
//             totalPages={data?.total_pages || 1}
//           />
//         </>
//       )}
//     </div>
//   )
// }


// import { useEffect } from 'react'
// import { useApi } from '../../hooks/useApi'
// import { Loader } from '../common/UI/Loader'
// import { Alert } from '../common/UI/Alert'

// export const SubmissionHistory = () => {
//   const { data: submissions, loading, error, get } = useApi()

//   useEffect(() => {
//     const fetchSubmissions = async () => {
//       try {
//         await get('/submissions/')
//       } catch (err) {
//         console.error('Failed to fetch submissions:', err)
//       }
//     }

//     fetchSubmissions()
//   }, [])

//   if (loading) return <Loader />
//   if (error) return <Alert type="error">Failed to load submissions</Alert>

//   if (!submissions || submissions.length === 0) {
//     return (
//       <div className="text-center text-gray-600">
//         You haven't submitted any solutions yet.
//       </div>
//     )
//   }

//   return (
//     <div className="space-y-4">
//       {submissions.map(submission => (
//         <div
//           key={submission.id}
//           className="bg-white rounded-lg shadow p-4"
//         >
//           <p><strong>Problem:</strong> {submission.problem_title}</p>
//           <p><strong>Status:</strong> {submission.status}</p>
//           <p><strong>Language:</strong> {submission.language}</p>
//           <p><strong>Submitted:</strong> {new Date(submission.created_at).toLocaleString()}</p>
//         </div>
//       ))}
//     </div>
//   )
// }


import { useEffect } from 'react'
import { useApi } from '../../hooks/useApi'
import { Loader } from '../common/UI/Loader'
import { Alert } from '../common/UI/Alert'

export const SubmissionHistory = () => {
  const { data, loading, error, get } = useApi()

  useEffect(() => {
    const fetchSubmissions = async () => {
      try {
        const result = await get('/submissions/history/')
        console.log("✅ Submissions fetched:", result)
      } catch (err) {
        console.error('❌ Failed to fetch submissions:', err)
      }
    }

    fetchSubmissions()
  }, [])

  const submissions = Array.isArray(data?.results) ? data.results : (Array.isArray(data) ? data : [])

  if (loading) return <Loader />
  if (error) return <Alert type="error">Failed to load submissions</Alert>

  if (submissions.length === 0) {
    return (
      <div className="text-center text-gray-600">
        You haven't submitted any solutions yet.
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {submissions.map(submission => (
        <div
          key={submission.id}
          className="bg-white rounded-lg shadow p-4"
        >
          <p><strong>Problem:</strong> {submission.problem_title}</p>
          <p><strong>Status:</strong> {submission.status}</p>
          <p><strong>Language:</strong> {submission.language_name}</p>
          <p><strong>Submitted:</strong> {new Date(submission.submitted_at || 'N/A').toLocaleString()}</p>
        </div>
      ))}
    </div>
  )
}
