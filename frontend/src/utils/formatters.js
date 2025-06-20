export const formatProblemData = (problem) => ({
  ...problem,
  truncatedDescription: truncateText(problem.description),
  difficultyClass: getDifficultyColor(problem.difficulty)
})

export const formatSubmissionData = (submission) => ({
  ...submission,
  formattedDate: formatDateTime(submission.submitted_at),
  executionTime: formatExecutionTime(submission.execution_time),
  statusClass: getStatusColor(submission.status)
})

export const formatUserData = (user) => ({
  ...user,
  displayName: user.username || user.email.split('@')[0],
  initials: user.username?.substring(0, 2).toUpperCase() || 'US'
})

export const formatLeaderboardData = (entries) => 
  entries.map((entry, index) => ({
    ...entry,
    rank: index + 1,
    formattedScore: `${entry.score}%`
  }))

export const formatCodeOutput = (output) => {
  const MAX_OUTPUT_LENGTH = 1000
  return output.length > MAX_OUTPUT_LENGTH
    ? output.substring(0, MAX_OUTPUT_LENGTH) + '\n... (truncated)'
    : output
}
