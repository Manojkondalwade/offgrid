# OffGrid Website Documentation

## 1. Overview

OffGrid is a role-based college event management website with three main user types:

- Student
- Organizer
- Sponsor

The website is now designed to work as a live full-stack application:

- The frontend is served from the `Frontend/` folder.
- The backend is a Flask API in `Backend/`.
- Authentication uses JWT tokens stored in browser local storage.
- Data is stored in SQLite by default.

The Flask app serves the frontend directly and exposes live APIs under `/api/*`.

## 2. Tech Stack

### Frontend

- HTML
- CSS
- Vanilla JavaScript

### Backend

- Flask
- Flask SQLAlchemy
- Flask JWT Extended
- Flask CORS
- SQLite

## 3. Application Architecture

### Frontend

The frontend lives in:

- `Frontend/`

Important frontend support files:

- `Frontend/js/auth.js`
  Handles session storage, authorization headers, role checks, and sign-out.
- `Frontend/js/app.js`
  Provides shared helpers such as toast notifications and route utilities.

### Backend

The backend lives in:

- `Backend/app/`

Main backend entry structure:

- `Backend/app/__init__.py`
  Creates the Flask app, registers blueprints, enables CORS, creates tables, and seeds demo users.

Registered API blueprints:

- `/api/auth`
- `/api/events`
- `/api/student`
- `/api/organizer`
- `/api/sponsor`

Health check:

- `/api/health`

## 4. User Roles

### Student

A student can:

- Sign up and sign in
- Browse published events
- View recommended events
- Register for events
- View registered events
- Vote in active time polls
- Manage profile and interests
- View live notifications based on registrations, polls, and recommendations

### Organizer

An organizer can:

- Sign up and sign in
- Create draft or published events
- Create poll-based events
- View organizer dashboard stats
- Manage events
- View analytics
- Review sponsor proposals
- Update organizer profile

### Sponsor

A sponsor can:

- Sign up and sign in
- Discover live events for sponsorship
- View match-based event recommendations
- Open event details
- Send sponsorship proposals
- Track sent proposals
- View sponsor dashboard metrics
- Update sponsor profile

## 5. Live Website Pages

### Public Pages

- `index.html`
  Landing page
- `login.html`
  Login and registration page

### Student Pages

- `student_dashboard.html`
  Live student dashboard
- `feed.html`
  Live recommended events feed
- `explore.html`
  Live published event discovery page
- `event_detail.html`
  Live event detail page
- `my_events.html`
  Live registration list
- `vote.html`
  Live poll voting page
- `notifications.html`
  Live notification summary page
- `student_profile.html`
  Live student profile editor

### Organizer Pages

- `dashboard.html`
  Live organizer dashboard
- `create_event.html`
  Live event creation page
- `event_manage.html`
  Live event management page
- `analytics.html`
  Live organizer analytics
- `proposals.html`
  Live organizer proposal inbox
- `sponsors.html`
  Live sponsor-connect overview
- `organizer_profile.html`
  Live organizer profile editor

### Sponsor Pages

- `sponsor_dashboard.html`
  Live sponsor dashboard
- `sponsor_events.html`
  Live sponsor event discovery
- `sponsor_event_detail.html`
  Live sponsor event detail and proposal submission
- `sponsor_proposals.html`
  Live sponsor proposal history
- `sponsor_profile.html`
  Live sponsor profile editor

## 6. Backend API Summary

### Auth API

Base path:

- `/api/auth`

Endpoints:

- `POST /register`
  Register a new user
- `POST /login`
  Log in and receive JWT token
- `GET /me`
  Get current user profile
- `PUT /me`
  Update current user profile

### Events API

Base path:

- `/api/events`

Endpoints:

- `GET /`
  Get public published or poll-active events
- `GET /<event_id>`
  Get full event details
- `GET /recommended`
  Get recommended events for logged-in user
- `GET /<event_id>/reviews`
  Get event reviews
- `POST /<event_id>/reviews`
  Add a review

### Student API

Base path:

- `/api/student`

Endpoints:

- `GET /dashboard`
  Student dashboard summary
- `GET /registrations`
  Get my registered events
- `POST /registrations`
  Register for an event
- `DELETE /registrations/<event_id>`
  Cancel event registration
- `GET /polls`
  Get active polls
- `POST /polls/<poll_id>/vote`
  Vote in a poll

### Organizer API

Base path:

- `/api/organizer`

Endpoints:

- `GET /dashboard`
  Organizer dashboard summary
- `GET /events`
  List organizer events
- `POST /events`
  Create event
- `PUT /events/<event_id>`
  Update event
- `DELETE /events/<event_id>`
  Delete event
- `GET /proposals`
  Get proposals for organizer events
- `PUT /proposals/<proposal_id>`
  Accept, reject, or discuss a proposal
- `GET /analytics`
  Organizer analytics

### Sponsor API

Base path:

- `/api/sponsor`

Endpoints:

- `GET /discover`
  Discover published events with match score and proposal status
- `GET /proposals`
  Get sponsor proposals
- `POST /proposals`
  Send sponsorship proposal
- `DELETE /proposals/<proposal_id>`
  Withdraw proposal
- `GET /dashboard`
  Sponsor dashboard summary

## 7. Authentication Flow

### Login

1. User opens `login.html`
2. User submits credentials
3. Frontend sends `POST /api/auth/login`
4. Backend returns:
   - JWT token
   - user object
5. Frontend stores both in local storage
6. User is redirected based on role:
   - Student -> `student_dashboard.html`
   - Organizer -> `dashboard.html`
   - Sponsor -> `sponsor_dashboard.html`

### Registration

1. User fills registration form
2. Frontend sends `POST /api/auth/register`
3. Backend creates the user and returns token plus profile
4. Frontend stores session and redirects to role dashboard

### Protected Pages

Protected pages use `OffGridAuth.requireRole(...)` from `Frontend/js/auth.js`.

If the token is missing or role is wrong:

- the user is signed out
- the user is redirected to `login.html`

## 8. Live Data Flow

### Event Publishing

1. Organizer creates an event from `create_event.html`
2. Frontend sends event data to `POST /api/organizer/events`
3. Backend stores the event
4. If poll options are included:
   - a poll is created
   - event status becomes `poll_active`
5. If published:
   - the event becomes visible on student and sponsor live pages

### Student Event Visibility

Published events now appear live in:

- `explore.html`
- `feed.html`
- `student_dashboard.html`
- `event_detail.html`

Student registration state is also live:

- A registered event shows `Registered`
- A non-registered event shows `Register`

### Sponsor Event Visibility

Published organizer events now appear live in:

- `sponsor_dashboard.html`
- `sponsor_events.html`
- `sponsor_event_detail.html`

## 9. Registration Behavior

Student registration works through:

- `POST /api/student/registrations`

After successful registration:

- the page reloads live registration state
- buttons update from `Register` to `Registered`
- success/error messages appear as in-page toast feedback

The browser alert popup behavior has been removed from the main registration flow.

## 10. Poll / Voting Behavior

If an organizer creates an event with time poll options:

- a live poll is created on the backend
- students can open `vote.html`
- students can vote through `POST /api/student/polls/<poll_id>/vote`

The voting page shows:

- active polls
- options
- current vote totals
- whether the student has already voted

## 11. Profile Management

All role profiles are now live and backed by:

- `GET /api/auth/me`
- `PUT /api/auth/me`

Pages:

- `student_profile.html`
- `organizer_profile.html`
- `sponsor_profile.html`

Supported live updates:

- name
- college
- branch
- year
- interests
- password

Fields differ slightly depending on role.

## 12. Database and Seed Data

Default database:

- SQLite
- `Backend/instance/offgrid.db`

Seed behavior:

- tables are created on app startup
- demo users are seeded only if the database is empty

Default seeded users:

- `student@college.edu` / `student123`
- `organizer@college.edu` / `organizer123`
- `sponsor@techcorp.in` / `sponsor123`
- `priya@college.edu` / `priya123`

## 13. Testing

The UI testing folder is:

- `test/`

Main files:

- `test/tester.js`
- `test/package.json`
- `test/report.html`

What the UI suite does:

- crawls discovered routes
- opens pages in Playwright
- tests visible buttons and forms
- checks console errors
- generates `report.html`

Recent improvements made to testing:

- hash-fragment duplicate routes are normalized
- hidden controls are skipped
- form submit buttons are handled more intelligently
- logout/sign-out buttons are skipped during QA clicking
- registration uses unique QA emails to avoid duplicate-signup false positives

## 14. Current Behavior Notes

- The website is now intended to behave as a live connected application.
- Organizer-published events should appear automatically across student and sponsor views.
- Registration and proposal actions now use in-page feedback instead of browser popup alerts in the main live flows.
- Some pages may still have simple layouts, but they are connected to live backend data.

## 15. Suggested Next Improvements

Recommended next steps for production readiness:

- Add server-side input validation rules for stronger data quality
- Add event detail links from more pages consistently
- Add review submission UI for students
- Add organizer-side event editing form UI
- Add richer notification persistence instead of computed notifications
- Clean up temporary QA users created by automated test runs
- Add route-level tests for every role flow
- Add pagination/filtering/sorting to large event and proposal lists

## 16. How To Run

Typical local flow:

1. Start the Flask backend
2. Open the app at:
   - `http://localhost:5000`
3. Sign in using one of the seeded accounts
4. Use the role-based dashboard

Health check:

- `http://localhost:5000/api/health`

## 17. File Map

Important files for maintenance:

- `Backend/app/__init__.py`
- `Backend/app/routes/auth.py`
- `Backend/app/routes/events.py`
- `Backend/app/routes/student.py`
- `Backend/app/routes/organizer.py`
- `Backend/app/routes/sponsor.py`
- `Backend/app/models/event.py`
- `Backend/app/models/proposal.py`
- `Backend/app/models/vote.py`
- `Backend/app/services/seed.py`
- `Frontend/js/auth.js`
- `Frontend/js/app.js`
- `Frontend/login.html`
- `Frontend/create_event.html`
- `Frontend/explore.html`
- `Frontend/feed.html`
- `Frontend/student_dashboard.html`
- `Frontend/my_events.html`
- `Frontend/vote.html`
- `Frontend/event_detail.html`
- `Frontend/dashboard.html`
- `Frontend/event_manage.html`
- `Frontend/analytics.html`
- `Frontend/proposals.html`
- `Frontend/sponsors.html`
- `Frontend/sponsor_dashboard.html`
- `Frontend/sponsor_events.html`
- `Frontend/sponsor_event_detail.html`
- `Frontend/sponsor_proposals.html`
- `Frontend/student_profile.html`
- `Frontend/organizer_profile.html`
- `Frontend/sponsor_profile.html`

---

If needed, this document can be split next into:

- User documentation
- Technical documentation
- API documentation
- Admin/setup documentation
