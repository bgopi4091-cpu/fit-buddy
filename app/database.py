from pathlib import Path

from sqlalchemy import Column, Float, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import DATABASE_URL

BASE_DIR = Path(__file__).resolve().parent.parent

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    username = Column(
        String(100),
        nullable=False,
    )

    age = Column(
        Integer,
        nullable=False,
    )

    weight = Column(
        Float,
        nullable=False,
    )

    goal = Column(
        String(200),
        nullable=False,
    )

    intensity = Column(
        String(100),
        nullable=False,
    )

    original_plan = Column(Text, nullable=True)

    updated_plan = Column(Text, nullable=True)
    nutrition_tip = Column(Text, nullable=True)
    feedback = Column(Text, nullable=True)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_user(db, user_id: str):
    return (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )


def save_user(
    db,
    username: str,
    user_id: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
):
    user = get_user(db, user_id)

    if user:
        user.username = username
        user.age = age
        user.weight = weight
        user.goal = goal
        user.intensity = intensity
    else:
        user = User(
            username=username,
            user_id=user_id,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )

        db.add(user)

    db.commit()
    db.refresh(user)

    return user


def save_plan(
    db,
    user_id: str,
    original_plan: str,
    nutrition_tip: str,
):
    user = get_user(db, user_id)

    if not user:
        return None

    user.original_plan = original_plan
    user.updated_plan = None
    user.nutrition_tip = nutrition_tip
    user.feedback = None

    db.commit()
    db.refresh(user)

    return user


def update_plan(
    db,
    user_id: str,
    updated_plan: str,
    feedback: str,
):
    user = get_user(db, user_id)

    if not user:
        return None

    user.updated_plan = updated_plan
    user.feedback = feedback

    db.commit()
    db.refresh(user)

    return user


def get_all_users(db):
    return (
        db.query(User)
        .order_by(User.id.desc())
        .all()
    )