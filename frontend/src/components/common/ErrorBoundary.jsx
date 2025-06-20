// src/components/common/ErrorBoundary.jsx
import React from 'react'

export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true }
  }

  componentDidCatch(error, errorInfo) {
    console.error("Error caught:", error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return <div className="text-red-600 p-4">Login form failed to load</div>
    }
    return this.props.children
  }
}
