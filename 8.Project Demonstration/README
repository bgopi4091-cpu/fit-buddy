# FitBuddy – AI Fitness Plan Generator

FitBuddy is a web-based fitness and wellness application that uses Google's Gemini API to generate personalized workout plans, nutrition/recovery guidance, and feedback-based plan updates. The application is built with FastAPI, Jinja2, SQLite, and SQLAlchemy.

## Project Information

- **Project Name:** FitBuddy
- **Team ID:** SWTID-2026-5836
- **Frontend:** HTML, CSS, JavaScript, Jinja2
- **Backend:** Python, FastAPI
- **Database:** SQLite with SQLAlchemy
- **AI Integration:** Google Gemini API using the Google GenAI SDK
- **Development Environment:** Visual Studio Code
- **Version Control:** Git and GitHub
- **Deployment:** Localhost using Uvicorn

## Key Features

- User fitness details form
- User and admin login
- AI-generated 7-day workout plan
- Personalized nutrition/recovery guidance
- Feedback-based workout plan regeneration
- User and plan data persistence using SQLite
- Admin dashboard for viewing users and plans
- Responsive web interface
- FastAPI interactive API documentation
- Health-check endpoint

## Technology Architecture

```text
User Browser
    |
    v
HTML / CSS / JavaScript / Jinja2
    |
    v
FastAPI + Uvicorn
    |
    +--------------------+
    |                    |
    v                    v
Google Gemini API    SQLAlchemy
    |                    |
    v                    v
Workout / Nutrition   SQLite Database
/ Feedback Updates
```

## Repository Structure

```text
fit-buddy/
├── app/                 # FastAPI application and backend logic
├── static/
│   └── css/             # Stylesheets
├── templates/           # Jinja2 HTML templates
├── tests/               # Automated smoke tests
├── .env.example         # Environment variable template
├── README.md            # Project documentation
├── requirements.txt     # Python dependencies
├── run.bat              # Windows batch run script
└── run.ps1              # PowerShell run script
```

## Requirements

- Python 3.10 or later
- Visual Studio Code or another Python IDE
- Internet connection for Gemini API requests
- Google Gemini API key

## Installation and Setup

### 1. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the Gemini API key

Copy `.env.example` to `.env`:

```cmd
copy .env.example .env
```

Open `.env` and add the API key:

```env
GEMINI_API_KEY=your_real_key_here
```

Do not upload or commit the `.env` file to GitHub.

## Running the Application

Start the FastAPI application with:

```bash
uvicorn app.main:app --reload
```

Then open:

- **Application:** http://127.0.0.1:8000
- **API Documentation:** http://127.0.0.1:8000/docs
- **Health Check:** http://127.0.0.1:8000/health
- **Admin:** http://127.0.0.1:8000/admin

## Testing

Automated smoke tests can be run using:

```bash
pytest
```

The tests check basic application startup and important routes without making a Gemini API request.

Manual testing includes:

1. Opening the home page.
2. Entering fitness details.
3. Generating a personalized 7-day workout plan.
4. Checking the nutrition/recovery guidance.
5. Submitting feedback and generating an updated plan.
6. Checking the admin dashboard.
7. Checking the API documentation and health endpoint.

## AI Features

FitBuddy uses the Google Gemini API to generate personalized fitness content. The AI component is used for:

- Workout plan generation
- Nutrition/recovery tips
- Feedback-based workout plan updates

The project uses Google's current `google-genai` SDK with configurable model names.

## Project Development Phases

The project follows the AI-ML-and-GEN-AI track workflow:

1. **Brainstorming & Ideation** – Identify the fitness guidance problem and propose FitBuddy.
2. **Requirement Analysis** – Define functional and non-functional requirements.
3. **Project Design Phase** – Prepare the solution architecture, data flow, journey map, and technology stack.
4. **Project Planning Phase** – Divide work into tasks, milestones, and responsibilities.
5. **Project Development Phase** – Build the FastAPI application, web interface, database, and Gemini integration.
6. **Project Testing** – Perform functional testing and automated smoke testing.
7. **Project Documentation** – Prepare project forms, technical documentation, README, and supporting deliverables.
8. **Project Demonstration** – Demonstrate the implemented features and explain the solution.

## Team Members

- Harini S
- Priya Dharshini S
- Manisha B
- Jaya Murugan V
- Harish S

## Future Enhancements

Possible future improvements include:

- Cloud deployment
- Migration from SQLite to PostgreSQL/MySQL for larger workloads
- Stronger authentication and security controls
- Mobile-friendly/PWA improvements
- Richer progress dashboards and analytics
- More advanced AI-based fitness personalization
- Performance and load testing for larger user volumes

## Important Note

FitBuddy provides general fitness and wellness information. It is not a substitute for professional medical advice.

## License

This project is an academic project developed for the AI-ML-and-GEN-AI project track.
