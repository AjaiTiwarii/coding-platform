import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { useApi } from '../../hooks/useApi'
import { ProblemCard } from './ProblemCard'
import { Loader } from '../common/UI/Loader'
import { Alert } from '../common/UI/Alert'
import { ProblemFilters } from './ProblemFilters'

export const ProblemList = () => {
  const [searchParams] = useSearchParams()
  const { loading, error, get } = useApi()
  const [problemList, setProblemList] = useState([])

  useEffect(() => {
    const fetchProblems = async () => {
      const params = Object.fromEntries(searchParams.entries())
      try {
        const result = await get('/problems/problems/', { params })
        console.log("Problems fetched:", result)
        setProblemList(result.results || [])
      } catch (err) {
        console.error("Failed to fetch problems:", err)
        setProblemList([])
      }
    }
    fetchProblems()
  }, [searchParams])

  return (
    <div className="space-y-4">
      <ProblemFilters />
      
      {loading && <Loader />}
      
      {error && (
        <Alert type="error">Failed to load problems: {error.message}</Alert>
      )}

      {!loading && !error && problemList.length > 0 && (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {problemList.map(problem => (
            <ProblemCard key={problem.id} problem={problem} />
          ))}
        </div>
      )}

      {!loading && !error && problemList.length === 0 && (
        <div className="text-center text-gray-500">No problems found.</div>
      )}
    </div>
  )
}
