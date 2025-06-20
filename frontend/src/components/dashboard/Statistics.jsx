import { useEffect, useRef } from 'react'
import { Chart } from 'chart.js/auto'
import { getDifficultyColor } from '../../utils/helpers'

export const Statistics = ({ data }) => {
  const chartRef = useRef(null)
  const progressChartRef = useRef(null)

  useEffect(() => {
    // Doughnut Chart - Problem Distribution
    if (
      data?.stats?.problems_solved_by_difficulty &&
      chartRef.current
    ) {
      const ctx = chartRef.current.getContext('2d')

      new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: ['Easy', 'Medium', 'Hard'],
          datasets: [{
            data: [
              data.stats.problems_solved_by_difficulty.easy ?? 0,
              data.stats.problems_solved_by_difficulty.medium ?? 0,
              data.stats.problems_solved_by_difficulty.hard ?? 0
            ],
            backgroundColor: [
              getDifficultyColor('EASY'),
              getDifficultyColor('MEDIUM'),
              getDifficultyColor('HARD')
            ]
          }]
        }
      })
    }

    // Line Chart - Activity Overview
    if (
      data?.activity_overview &&
      progressChartRef.current
    ) {
      const ctx = progressChartRef.current.getContext('2d')

      new Chart(ctx, {
        type: 'line',
        data: {
          labels: data.activity_overview.labels ?? [],
          datasets: [{
            label: 'Submissions',
            data: data.activity_overview.data ?? [],
            borderColor: '#3B82F6',
            tension: 0.4
          }]
        }
      })
    }
  }, [data])

  // Fallback for missing data
  if (!data?.stats) {
    return (
      <div className="p-6 text-red-600">
        Unable to load dashboard statistics.
      </div>
    )
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm space-y-8">
      <div>
        <h2 className="text-xl font-semibold mb-4">Solved Problems</h2>
        <div className="grid grid-cols-3 gap-4">
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-2xl font-bold text-green-600">
              {data?.stats?.total_solved ?? 0}
            </div>
            <div className="text-sm text-green-800">Total Solved</div>
          </div>
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <div className="text-2xl font-bold text-blue-600">
              {data?.stats?.success_rate ?? 0}%
            </div>
            <div className="text-sm text-blue-800">Acceptance Rate</div>
          </div>
          <div className="text-center p-4 bg-purple-50 rounded-lg">
            <div className="text-2xl font-bold text-purple-600">
              {data?.stats?.current_streak ?? 0}
            </div>
            <div className="text-sm text-purple-800">Day Streak</div>
          </div>
        </div>
      </div>

      <div>
        <h2 className="text-xl font-semibold mb-4">Problem Distribution</h2>
        <canvas ref={chartRef} />
      </div>

      <div>
        <h2 className="text-xl font-semibold mb-4">Activity Overview</h2>
        <canvas ref={progressChartRef} />
      </div>
    </div>
  )
}
