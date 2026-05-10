# Smart Task Management System

A modern Flask-based Smart Task Management System with authentication, PostgreSQL integration, analytics, and real-time notifications using WebSockets.

---

# Features

- User Registration & Login
- Secure Password Authentication
- Add / Update / Delete Tasks
- REST API Integration
- PostgreSQL Database
- Analytics Dashboard using Pandas & NumPy
- Real-time Notifications using Flask-SocketIO
- Responsive Modern UI
- Task Status & Priority Management

---

# Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-SocketIO
- PostgreSQL
- Pandas
- NumPy
- HTML
- CSS
- JavaScript

---

# Project Structure

```bash
smart-task-manager/
│
├── static/
├── templates/
├── app.py
├── analytics.py
├── config.py
├── models.py
├── requirements.txt
├── taskdb_schema.sql
└── README.md
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone https://github.com/Aravindhaloshan/task_manager.git
cd smart-task-manager
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\\Scripts\\activate
```

### Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Create PostgreSQL Database

Open PostgreSQL:

```sql
CREATE DATABASE taskdb;
```

---

## 5. Update Database Configuration

Open `config.py`

```python
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/taskdb'
```

Replace:
- postgres username
- password

with your PostgreSQL credentials.

---

## 6. Run Application

```bash
python app.py
```

---

# APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | /add-task | Add task |
| POST | /update-task/<id> | Update task |
| POST | /delete-task/<id> | Delete task |
| GET | /tasks | Get all tasks |

---

# Analytics

The dashboard displays:
- Total Tasks
- Completed Tasks
- Pending Tasks
- Completion Percentage

using:
- Pandas
- NumPy

---

# WebSocket Feature

Real-time task notifications implemented using:
- Flask-SocketIO

---

# Author

Aravindha Loshan
aravindhaloshan02@gmail.com
