from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import init_db
from app.routes import router

app = FastAPI(
    title="FitBuddy AI Fitness Planner",
    description="AI-powered personalized fitness planning application",
    version="1.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

app.include_router(router)


@app.on_event("startup")
def startup():
    init_db()