# Frontend - Coding Platform (React + TailwindCSS)

This is the **frontend** of the full-stack coding platform built with **React**, **TailwindCSS**, and **Axios** for consuming the Django REST APIs. It allows users to register, solve problems, view submissions, and manage their dashboard.

---

## 🚀 Getting Started

### 1. Navigate to Frontend

```bash
cd coding_platform/frontend
```

### 2. Install Node.js Dependencies

```bash
npm install
```

### 3. Environment Setup

Create a `.env` file:

Configure:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

### 4. Start Development Server

```bash
npm run dev
```

---

## 🧩 Features

- User authentication (Login/Register)
- Responsive problem listing page
- Monaco code editor integration
- Language selection
- Code submission + result display
- Submission history tracking
- Dashboard with user stats

---

## ⚙️ Project Structure

```
coding_platform/frontend/
├── public/                 # Static files
├── src/
│   ├── components/         # UI components
│   ├── pages/              # Route pages
│   ├── hooks/              # Custom React hooks
│   ├── services/           # Axios API services
│   ├── context/            # Auth and Theme contexts
│   ├── styles/             # Tailwind and custom styles
│   └── App.jsx
├── .env.example            # Example env file
├── package.json            # Dependencies
```

---

## 🔐 Authentication

Uses JWT tokens to manage session:

- `authToken` stored in localStorage
- Auto-refresh on 401 using interceptors

---

## 📦 API Communication

Handled using Axios instance inside `src/services/api.js`


## 📜 License

This project is open-source and available under the [MIT License](../LICENSE).

