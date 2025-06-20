# Backend - Coding Platform (Django REST Framework)

This is the **backend** of the full-stack coding platform built with **Django**, **Django REST Framework**, and **Celery** for asynchronous code evaluation. It provides APIs for user authentication, problem management, and submission handling, including secure code execution using subprocesses.

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/coding-platform.git
cd coding-platform/backend
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements/development.txt
```


### 5. Apply Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

---

## 🧩 Features

- JWT Authentication
- User registration & profile
- Admin interface
- Problem CRUD (with tags, difficulty)
- Code submission & test case evaluation
- Subprocess-based code execution (Python, C++)
- Celery-based async execution

---

## 🧠 Project Structure

```
coding_platform/backend
├── apps
│   ├── authentication/     # User models and auth APIs
│   ├── problems/           # Problems and test cases
│   ├── submissions/        # Code submissions and evaluation
│   └── dashboard/          # User stats and performance
├── coding_platform         # Django project config
│   ├── settings/           # Base, dev, and prod settings
├── utils/                  # Permissions, exceptions, constants
├── requirements/           # requirements/*.txt
├── manage.py
```

---

## 🔄 Celery + Redis Setup (Async Code Execution)

Start the Celery worker:
```bash
celery -A coding_platform worker --loglevel=info
```

Make sure Redis is running on port `6379`.

---

## 🧪 Sample API Endpoints

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `GET /api/problems/`
- `POST /api/submissions/submit/`
- `GET /api/submissions/history/`

---

## 📜 License

This project is open-source and available under the [MIT License](../LICENSE).

