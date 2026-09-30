from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import ADMIN_PASSWORD, MAX_FEEDBACK_LENGTH
from app.database import (
    get_all_users,
    get_db,
    get_user,
    save_plan,
    save_user,
    update_plan,
)
from app.gemini_client import (
    generate_nutrition_tip_with_flash,
    generate_workout_gemini,
    update_workout_plan,
)
from app.schemas import (
    FeedbackRequest,
    FeedbackResponse,
    GenerateResponse,
    UserInput,
)

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "error": None,
        },
    )


@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        user = save_user(
            db,
            username=username,
            user_id=user_id,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )

        workout_plan = generate_workout_gemini(
            username=username,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )

        nutrition_tip = generate_nutrition_tip_with_flash(
            goal
        )

        save_plan(
            db,
            user_id=user_id,
            original_plan=workout_plan,
            nutrition_tip=nutrition_tip,
        )

        user = get_user(db, user_id)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "request": request,
                "user": user,
                "workout_plan": workout_plan,
                "nutrition_tip": nutrition_tip,
                "message": "Your personalized plan is ready.",
                "error": None,
            },
        )

    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "request": request,
                "error": str(exc),
            },
            status_code=500,
        )


@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db),
):
    feedback = feedback.strip()

    user = get_user(db, user_id)

    if not user:
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "request": request,
                "user": None,
                "workout_plan": None,
                "nutrition_tip": None,
                "message": None,
                "error": "User ID not found.",
            },
            status_code=404,
        )

    if len(feedback) < 3:
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "request": request,
                "user": user,
                "workout_plan": user.updated_plan
                or user.original_plan,
                "nutrition_tip": user.nutrition_tip,
                "message": None,
                "error": "Feedback must contain at least 3 characters.",
            },
            status_code=400,
        )

    if len(feedback) > MAX_FEEDBACK_LENGTH:
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "request": request,
                "user": user,
                "workout_plan": user.updated_plan
                or user.original_plan,
                "nutrition_tip": user.nutrition_tip,
                "message": None,
                "error": (
                    f"Feedback cannot exceed "
                    f"{MAX_FEEDBACK_LENGTH} characters."
                ),
            },
            status_code=400,
        )

    try:
        current_plan = (
            user.updated_plan
            or user.original_plan
        )

        revised_plan = update_workout_plan(
            original_plan=current_plan,
            feedback=feedback,
            goal=user.goal,
            intensity=user.intensity,
        )

        update_plan(
            db,
            user_id=user_id,
            updated_plan=revised_plan,
            feedback=feedback,
        )

        user = get_user(db, user_id)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "request": request,
                "user": user,
                "workout_plan": revised_plan,
                "nutrition_tip": user.nutrition_tip,
                "message": "Workout plan updated successfully.",
                "error": None,
            },
        )

    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "request": request,
                "user": user,
                "workout_plan": user.updated_plan
                or user.original_plan,
                "nutrition_tip": user.nutrition_tip,
                "message": None,
                "error": str(exc),
            },
            status_code=500,
        )


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(
    request: Request,
    admin_password: str = "",
    db: Session = Depends(get_db),
):
    if admin_password != ADMIN_PASSWORD:
        return templates.TemplateResponse(
            request=request,
            name="admin_login.html",
            context={
                "request": request,
                "error": "Invalid admin password.",
            },
            status_code=401,
        )

    users = get_all_users(db)

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "request": request,
            "users": users,
        },
    )


@router.post(
    "/api/generate-workout",
    response_model=GenerateResponse,
)
def api_generate_workout(
    payload: UserInput,
    db: Session = Depends(get_db),
):
    workout_plan = generate_workout_gemini(
        username=payload.username,
        age=payload.age,
        weight=payload.weight,
        goal=payload.goal,
        intensity=payload.intensity,
    )

    nutrition_tip = generate_nutrition_tip_with_flash(
        payload.goal
    )

    save_user(
        db,
        **payload.model_dump(),
    )

    save_plan(
        db,
        user_id=payload.user_id,
        original_plan=workout_plan,
        nutrition_tip=nutrition_tip,
    )

    return GenerateResponse(
        user_id=payload.user_id,
        workout_plan=workout_plan,
        nutrition_tip=nutrition_tip,
    )


@router.post(
    "/api/submit-feedback",
    response_model=FeedbackResponse,
)
def api_submit_feedback(
    payload: FeedbackRequest,
    db: Session = Depends(get_db),
):
    user = get_user(
        db,
        payload.user_id,
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User ID not found.",
        )

    feedback = payload.feedback.strip()

    if len(feedback) < 3:
        raise HTTPException(
            status_code=400,
            detail="Feedback must contain at least 3 characters.",
        )

    if len(feedback) > MAX_FEEDBACK_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Feedback cannot exceed "
                f"{MAX_FEEDBACK_LENGTH} characters."
            ),
        )

    current_plan = (
        user.updated_plan
        or user.original_plan
    )

    revised_plan = update_workout_plan(
        original_plan=current_plan,
        feedback=feedback,
        goal=user.goal,
        intensity=user.intensity,
    )

    update_plan(
        db,
        user_id=payload.user_id,
        updated_plan=revised_plan,
        feedback=feedback,
    )

    return FeedbackResponse(
        user_id=payload.user_id,
        updated_plan=revised_plan,
    )


@router.get("/api/users")
def api_users(
    admin_password: str = "",
    db: Session = Depends(get_db),
):
    if admin_password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=401,
            detail="Invalid admin password.",
        )

    users = get_all_users(db)

    return JSONResponse(
        content=[
            {
                "user_id": user.user_id,
                "username": user.username,
                "age": user.age,
                "weight": user.weight,
                "goal": user.goal,
                "intensity": user.intensity,
                "original_plan": user.original_plan,
                "updated_plan": user.updated_plan,
                "nutrition_tip": user.nutrition_tip,
                "feedback": user.feedback,
            }
            for user in users
        ]
    )


@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "fitbuddy",
    }