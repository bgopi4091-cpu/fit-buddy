# FitBuddy – AI Fitness Plan Generator

FitBuddy is a FastAPI + Jinja2 + SQLite application based on the supplied project documentation. It generates personalized 7-day workout plans, nutrition/recovery tips, and feedback-driven plan revisions using Google Gemini.

## Architecture

- Frontend: HTML + Jinja2 + CSS
- Backend: FastAPI
- AI: Google Gemini through the `google-genai` SDK
- Database: SQLite + SQLAlchemy
- API docs: FastAPI `/docs`
- Admin view: `/view-all-users?admin_password=...`

The original documentation names Gemini 1.5 Pro and Gemini Flash. Model availability changes over time, so the application makes model names configurable in `.env`; the default is `gemini-2.5-flash`.

## Project structure

```text
fitbuddy/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── gemini_client.py
│   ├── main.py
│   ├── routes.py
│   └── schemas.py
├── static/
│   └── style.css
├── templates/
│   ├── admin_login.html
│   ├── all_users.html
│   ├── index.html
│   └── result.html
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── tests/
    ├── __init__.py
    └── test_app.py
```

## Windows / VS Code setup

1. Install Python 3.11+ and VS Code.
2. Open this `fitbuddy` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment:

```powershell
python -m venv venv
```

5. Activate it:

```powershell
venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```cmd
venv\Scripts\activate
```

6. Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

7. Copy `.env.example` to `.env`.
8. Put your Google Gemini API key into `GOOGLE_API_KEY`.
9. Change `ADMIN_PASSWORD`.
10. Start the server:

```powershell
uvicorn app.main:app --reload
```

11. Open:
   - App: http://127.0.0.1:8000
   - Swagger API docs: http://127.0.0.1:8000/docs
   - ReDoc: http://127.0.0.1:8000/redoc

## Testing

Run:

```powershell
pytest -q
```

The included tests verify the health route, database persistence, and the HTML home page without making real Gemini calls.

## API examples

### Generate

`POST /api/generate-workout`

JSON:

```json
{
  "username": "Alex",
  "user_id": "FB001",
  "age": 25,
  "weight": 70,
  "goal": "muscle gain",
  "intensity": "medium"
}
```

### Update with feedback

`POST /api/submit-feedback`

```json
{
  "user_id": "FB001",
  "feedback": "Add more cardio and include one rest day."
}
```

### Admin API

`GET /api/users?admin_password=YOUR_PASSWORD`

For production, replace query-string password authentication with a proper authenticated admin account/session.

## Notes

This is a general wellness application, not a medical device. AI-generated exercise and nutrition content should be reviewed by a qualified professional when a user has medical conditions, injuries, or other special circumstances.
