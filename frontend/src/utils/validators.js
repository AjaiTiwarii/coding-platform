export const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!re.test(String(email).toLowerCase())) {
    return 'Invalid email address'
  }
}

export const validateUsername = (username) => {
  if (username.length < 3) return 'Username must be at least 3 characters'
  if (!/^[a-zA-Z0-9_]+$/.test(username)) {
    return 'Username can only contain letters, numbers and underscores'
  }
}

export const validatePassword = (password) => {
  if (password.length < 8) return 'Password must be at least 8 characters'
  if (!/[A-Z]/.test(password)) return 'Must contain at least one uppercase letter'
  if (!/[0-9]/.test(password)) return 'Must contain at least one number'
}

export const validateCode = (code) => {
  if (code.length < 10) return 'Code must be at least 10 characters'
  if (code.length > 50000) return 'Code exceeds maximum length'
}

export const validateTestInput = (input) => {
  if (input.length > 10000) return 'Input exceeds maximum length'
}

export const validateConfirmPassword = (password, confirmPassword) => {
  if (password !== confirmPassword) return 'Passwords do not match'
}
