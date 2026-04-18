# OffGrid — College Event Management Platform

> One platform for students, clubs, and sponsors to discover, manage, and fund college events.

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| 🎯 Personalized Event Feed | Recommendations based on student interests |
| 🗳️ Time Polling System | Students vote on preferred event timings |
| 🤝 Sponsor Connect | Clubs post events, sponsors browse & propose |
| 📊 Organizer Analytics | Registration trends, poll insights, heatmaps |
| 🔔 Smart Notifications | Real-time updates for events and polls |
| 🔐 Role-based Auth | Student / Organizer / Sponsor dashboards |

---

## 🏗️ Project Structure

```
offgrid-platform/
├── Frontend/                 # Pure HTML/CSS/JS prototype (18 pages)
│   ├── index.html            # Landing page
│   ├── login.html            # Role-based auth
│   ├── student_dashboard.html
│   ├── dashboard.html        # Organizer dashboard
│   ├── sponsor_dashboard.html
│   ├── feed.html / explore.html / event_detail.html
│   ├── vote.html             # Time polling
│   ├── analytics.html        # Charts & metrics
│   ├── proposals.html        # Sponsor proposals inbox
│   ├── notifications.html
│   ├── css/ (main.css, dashboard.css, feed.css)
│   └── js/  (data.js, app.js, auth.js, vote.js...)
│
├── Backend/                  # Flask REST API
│   ├── run.py                # Entry point
│   └── app/
│       ├── __init__.py       # App factory
│       ├── config.py
│       ├── models/           # SQLAlchemy models
│       │   ├── user.py
│       │   ├── event.py
│       │   ├── registration.py
│       │   ├── vote.py       # Poll + PollOption + Vote
│       │   ├── proposal.py
│       │   └── review.py
│       ├── routes/           # Flask blueprints
│       │   ├── auth.py       # /api/auth/*
│       │   ├── events.py     # /api/events/*
│       │   ├── student.py    # /api/student/*
│       │   ├── organizer.py  # /api/organizer/*
│       │   └── sponsor.py    # /api/sponsor/*
│       ├── services/
│       │   ├── seed.py       # Demo data seeder
│       │   └── recommendations.py
│       └── utils/
│           └── helpers.py
│
├── Database/
│   ├── schema_notes.md       # Table definitions
│   ├── seed_data.json        # Sample data
│   └── firestore_rules.txt   # For Firebase migration
│
├── requirements.txt
└── .env.example
```

---

## ⚡ Quick Start

### 1. Frontend (No server needed)
```
Open Frontend/index.html in any browser
```

**Demo Logins (in login.html):**
| Role | Email | Password |
|------|-------|----------|
| Student | `student@college.edu` | `student123` |
| Organizer | `organizer@college.edu` | `organizer123` |
| Sponsor | `sponsor@techcorp.in` | `sponsor123` |

---

### 2. Backend (Flask API)

```bash
# Clone / navigate to project
cd offgrid-platform

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Set up environment
copy .env.example .env

# Run the server
cd Backend
python run.py
```

API will start at: **http://localhost:5000**

Health check: `GET http://localhost:5000/api/health`

---

## 📡 API Endpoints

### Auth (`/api/auth`)
| Method | Route | Description |
|--------|-------|-------------|
| POST | `/register` | Create account |
| POST | `/login` | Sign in → returns JWT |
| GET  | `/me` | Get profile (JWT required) |
| PUT  | `/me` | Update profile (JWT required) |

### Events (`/api/events`)
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | List all published events |
| GET | `/<id>` | Single event + poll + reviews |
| GET | `/recommended` | Personalized recommendations (JWT) |
| POST | `/<id>/reviews` | Post review (JWT) |

### Student (`/api/student`)
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/dashboard` | Stats summary (JWT) |
| GET | `/registrations` | My registered events (JWT) |
| POST | `/registrations` | Register for event (JWT) |
| DELETE | `/registrations/<id>` | Cancel registration (JWT) |
| GET | `/polls` | Active polls with my vote (JWT) |
| POST | `/polls/<id>/vote` | Cast a vote (JWT) |

### Organizer (`/api/organizer`)
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/dashboard` | Club overview (JWT) |
| GET | `/events` | My events (JWT) |
| POST | `/events` | Create event + optional poll (JWT) |
| PUT | `/events/<id>` | Update event (JWT) |
| DELETE | `/events/<id>` | Delete event (JWT) |
| GET | `/proposals` | Incoming proposals (JWT) |
| PUT | `/proposals/<id>` | Accept / reject (JWT) |
| GET | `/analytics` | Registration analytics (JWT) |

### Sponsor (`/api/sponsor`)
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/dashboard` | Sponsor overview (JWT) |
| GET | `/discover` | Events matching interests (JWT) |
| GET | `/proposals` | My sent proposals (JWT) |
| POST | `/proposals` | Send proposal (JWT) |
| DELETE | `/proposals/<id>` | Withdraw proposal (JWT) |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, Vanilla CSS, JavaScript (ES6) |
| Backend | Python 3.11, Flask 3.0 |
| Database | SQLite (dev) → PostgreSQL ready |
| Auth | JWT (flask-jwt-extended) |
| ORM | SQLAlchemy |
| CORS | flask-cors |

---

## 👥 Team / Hackathon

Built for **CodeDecode Hackathon 2025** — OffGrid prototype demonstrating a college-first event management ecosystem.