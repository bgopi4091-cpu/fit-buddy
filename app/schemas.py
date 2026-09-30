from pydantic import BaseModel, Field


class UserInput(BaseModel):
    username: str = Field(min_length=2, max_length=100)
    user_id: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=13, le=100)
    weight: float = Field(gt=20, le=400)
    goal: str = Field(min_length=2, max_length=200)
    intensity: str = Field(min_length=2, max_length=100)


class GenerateResponse(BaseModel):
    user_id: str
    workout_plan: str
    nutrition_tip: str


class FeedbackRequest(BaseModel):
    user_id: str
    feedback: str = Field(min_length=3, max_length=1500)


class FeedbackResponse(BaseModel):
    user_id: str
    updated_plan: str