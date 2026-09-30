import os
from pathlib import Path

os.environ["DATABASE_URL"] = "sqlite:///./test_fitbuddy.db"
os.environ["ADMIN_PASSWORD"] = "test-password"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

TEST_DB = "sqlite:///./test_fitbuddy.db"
engine = create_engine(TEST_DB, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def setup_module():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def teardown_module():
    Base.metadata.drop_all(engine)
    Path("test_fitbuddy.db").unlink(missing_ok=True)


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


def test_home():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert "FitBuddy" in response.text


def test_admin_requires_password():
    with TestClient(app) as client:
        response = client.get("/api/users?admin_password=wrong")
        assert response.status_code == 401
