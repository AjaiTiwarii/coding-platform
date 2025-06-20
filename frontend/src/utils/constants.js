export const DIFFICULTY = {
  EASY: 'Easy',
  MEDIUM: 'Medium',
  HARD: 'Hard'
}

export const SUBMISSION_STATUS = {
  PENDING: 'Pending',
  ACCEPTED: 'Accepted',
  WRONG_ANSWER: 'Wrong Answer',
  TIME_LIMIT_EXCEEDED: 'Time Limit Exceeded',
  MEMORY_LIMIT_EXCEEDED: 'Memory Limit Exceeded',
  COMPILATION_ERROR: 'Compilation Error',
  RUNTIME_ERROR: 'Runtime Error'
}

// export const API_ENDPOINTS = {
//   PROBLEMS: '/api/problems/',
//   SUBMISSIONS: '/api/submissions/',
//   AUTH: {
//     LOGIN: '/api/auth/login/',
//     REGISTER: '/api/auth/register/',
//     PROFILE: '/api/auth/profile/'
//   }
// }

export const API_ENDPOINTS = {
  PROBLEMS: '/problems/',
  SUBMISSIONS: '/submissions/',
  AUTH: {
    LOGIN: '/auth/login/',
    REGISTER: '/auth/register/',
    PROFILE: '/auth/profile/'
  }
}

export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 20,
  PROBLEMS_PER_PAGE: 25,
  SUBMISSIONS_PER_PAGE: 50
}

export const EDITOR_CONFIG = {
  DEFAULT_THEME: 'vs-dark',
  DEFAULT_LANGUAGE: 'python',
  FONT_SIZES: [12, 14, 16, 18, 20],
  TAB_SIZES: [2, 4, 6, 8]
}

export const USER_ROLES = {
  STUDENT: 'student',
  ADMIN: 'admin',
  JUDGE: 'judge'
}
