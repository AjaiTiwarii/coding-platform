# Full-Stack Coding Platform

This is the **full-stack coding platform** project built with **Django**, **React**, **Tailwind CSS**, and **Celery**. It enables users to browse coding problems, write and submit code online, and get real-time verdicts.

---

## 🚀 Features

- User Authentication (JWT)
- Coding Problem Management
- Sample + Hidden Test Case Support
- Monaco Code Editor (Python, C++ supported)
- Subprocess-based Local Code Execution (No external APIs)
- Verdicts: Accepted, Compilation Error, Runtime Error, etc.
- Async Processing with Celery + Redis
- Submission History + Score Calculation

---

## 🔧 Tech Stack

### Backend
- Django + Django REST Framework
- PostgreSQL
- Redis + Celery
- Python/Django `subprocess` for code execution

### Frontend
- React (Vite)
- Tailwind CSS
- Axios + React Hooks
- Monaco Editor

---

## 📁 Project Structure

```
coding_platform/
├── backend/            # Django backend
│   ├── apps/           # Apps: auth, problems, submissions, dashboard
│   ├── settings/       # Environment configs
│   ├── utils/          # Permissions, helpers, constants
│   └── manage.py
├── frontend/           # React frontend
│   └── src/            # Components, pages, services, hooks
├── deployment/         
├── docs/               # Docs: API, deployment, architecture
├── README.md           # ← This file
├── .env.example        # Env template
└── .gitignore
```

---

## 📄 Setup Instructions

### Clone and Navigate
```bash
git clone https://github.com/your-username/coding-platform.git
cd coding-platform
```

### Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements/development.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

### Celery Worker
```bash
celery -A coding_platform worker --loglevel=info
```

Make sure Redis is running.

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 🔬 Example API Endpoints

- `POST   /api/auth/login/`
- `POST   /api/auth/register/`
- `GET    /api/problems/`
- `POST   /api/submissions/submit/`
- `GET    /api/submissions/history/`

---

## 🔄 Code Evaluation Flow

1. User writes code in the editor
2. Submits code via `/submissions/submit/`
3. Backend saves submission & spawns `subprocess` execution
4. Each test case is fed as input
5. Output is compared to expected output
6. Verdict is saved + returned to frontend

---

## 🌐 Related READMEs

- [`frontend/frontend_readme.md`](./frontend/frontend_readme.md) — React setup & scripts
- [`backend/backend_readme.md`](./backend/backend_readme.md) — Django + Celery setup

---


## 📖 License

This project is licensed under the [MIT License](./LICENSE).

