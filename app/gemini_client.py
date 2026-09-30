import time

from google import genai

from app.config import (
    GOOGLE_API_KEY,
    GEMINI_WORKOUT_MODEL,
    GEMINI_TIP_MODEL,
)


def get_client():
    if not GOOGLE_API_KEY:
        raise RuntimeError(
            "GOOGLE_API_KEY is missing."
        )

    return genai.Client(
        api_key=GOOGLE_API_KEY
    )


def _generate(
    model: str,
    prompt: str,
    max_retries: int = 3,
) -> str:

    client = get_client()

    last_error = None

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )

            text = getattr(
                response,
                "text",
                None,
            )

            if not text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return text.strip()

        except Exception as exc:

            last_error = exc

            error_text = str(exc)

            # Retry temporary Google server errors.
            if (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "high demand" in error_text
            ):

                if attempt < max_retries - 1:

                    wait_time = (
                        2 ** attempt
                    )

                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue

            raise

    raise RuntimeError(
        f"Gemini request failed: {last_error}"
    )


def generate_workout_gemini(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
) -> str:

    prompt = f"""
You are FitBuddy, an AI fitness planning assistant.

Create a practical 7-day workout plan.

User:
Name: {username}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}

Requirements:

1. Monday through Sunday.
2. Exercises.
3. Sets and repetitions or duration.
4. Warm-up guidance.
5. Cool-down guidance.
6. At least one rest/recovery day.
7. Keep the plan realistic.
8. Do not diagnose medical conditions.
9. Do not prescribe medication.
10. Include a short safety reminder.

Use clear headings and bullet points.

Return only the workout plan.
"""

    return _generate(
        GEMINI_WORKOUT_MODEL,
        prompt,
    )


def generate_nutrition_tip_with_flash(
    goal: str,
) -> str:

    prompt = f"""
You are FitBuddy, an AI fitness assistant.

Fitness goal:

{goal}

Provide:

1. General nutrition guidance.
2. Hydration guidance.
3. Recovery and sleep guidance.
4. A short safety reminder.

Keep the advice general and practical.

Do not diagnose medical conditions.
Do not prescribe medication.

Use clear headings.
"""

    return _generate(
        GEMINI_TIP_MODEL,
        prompt,
    )


def update_workout_plan(
    original_plan: str,
    feedback: str,
    goal: str,
    intensity: str,
) -> str:

    prompt = f"""
You are FitBuddy, an AI fitness planning assistant.

Fitness goal:
{goal}

Preferred intensity:
{intensity}

Current workout plan:

{original_plan}

User feedback:

{feedback}

Create a revised 7-day workout plan.

Requirements:

1. Address the feedback.
2. Keep useful parts of the current plan.
3. Include Monday through Sunday.
4. Include exercises.
5. Include sets/repetitions or duration.
6. Include warm-up.
7. Include cool-down.
8. Include recovery/rest.
9. Keep the plan realistic.
10. Do not diagnose medical conditions.
11. Do not prescribe medication.

Return only the revised workout plan.
"""

    return _generate(
        GEMINI_WORKOUT_MODEL,
        prompt,
    )