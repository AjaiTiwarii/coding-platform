import { Routes, Route } from 'react-router-dom'
import { Layout } from './components/common/Layout/Layout'
import { useAuth } from './hooks/useAuth'
import { useTheme } from './context/ThemeContext'
import { DashboardPage } from './pages/Dashboard'
import { ProblemsPage } from './pages/Problems'
import { LoginPage } from './pages/auth/Login'
import { RegisterPage } from './pages/auth/Register'
import { Loader } from './components/common/UI/Loader'
import { ProblemSolvePage } from './pages/ProblemSolve'
import { ProfilePage } from './pages/Profile'
import { SubmissionsPage } from './pages/Submissions'


export const App = () => {

  const { loading } = useAuth()
  const { theme } = useTheme()

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">
      <Loader size="lg" />
    </div>
  }



  return (
    <div className={theme}>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<DashboardPage />} />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="problems" element={<ProblemsPage />} />
          <Route path="problems/:id" element={<ProblemSolvePage />} />
          <Route path="login" element={<LoginPage />} />
          <Route path="register" element={<RegisterPage />} />
          <Route path="profile" element={<ProfilePage />} />
          <Route path="submissions" element={<SubmissionsPage/>}/>
        </Route>
      </Routes>
    </div>
  )
}
