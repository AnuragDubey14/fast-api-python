import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.db import Base  # Your SQLAlchemy Base
from dependencies import get_db  # Original dependency
from app import app  # Your FastAPI app instance
import time

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:1234@localhost:3306/test_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clean slate for tests
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# Helper: get auth header without pre-hashing
def get_auth_header(username: str, password: str):
    response = client.post("/token", data={"username": username, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_register_user():
    response = client.post(
        "/register",
        json={"user_name": "testuser", "user_password": "testpass"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["user_name"] == "testuser"
    assert "user_id" in data

def test_login_user():
    client.post(
        "/register",
        json={"user_name": "loginuser", "user_password": "loginpass"}
    )
    response = client.post(
        "/token",
        data={"username": "loginuser", "password": "loginpass"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_add_task():
    client.post(
        "/register",
        json={"user_name": "taskuser", "user_password": "taskpass"}
    )
    headers = get_auth_header("taskuser", "taskpass")
    now = datetime.now().isoformat()
    task_payload = {
        "title": "Test Task",
        "description": "Task description",
        "status": False,
        "created_at": now,
        "updated_at": now,
        "deadline": now,
        "owner_id":"taskuser"
    }
    response = client.post("/task/", json=task_payload, headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    print("RESPONSE JSON:ADD_TASK ",data)
    assert data["message"] == "Task added successfully"
    assert data["task"]["title"] == "Test Task"
    assert data["task"]["owner_id"] is not None

def test_update_task():
    headers = get_auth_header("taskuser", "taskpass")
    now = datetime.now().isoformat()
    task_payload = {
        "title": "Update Task",
        "description": "Old description",
        "status": False,
        "created_at": now,
        "updated_at": now,
        "deadline": now
    }
    response = client.post("/task/", json=task_payload, headers=headers)
    task = response.json()["task"]
    task_id = task["task_id"]
    
    updated_payload = {
        "title": "Update Task",
        "description": "New description",
        "status": True,
        "created_at": now,
        "updated_at": now,
        "deadline": now
    }
    response = client.put(f"/task/?id={task_id}", json=updated_payload, headers=headers)
    assert response.status_code == 200, response.text
    updated_task = response.json()
    assert updated_task["description"] == "New description"
    assert updated_task["status"] is True

def test_update_status():
    headers = get_auth_header("taskuser", "taskpass")
    now = datetime.now().isoformat()
    task_payload = {
        "title": "Status Task",
        "description": "Old description",
        "status": False,
        "created_at": now,
        "updated_at": now,
        "deadline": now
    }
    response = client.post("/task/", json=task_payload, headers=headers)
    task = response.json()["task"]
    task_id = task["task_id"]
    
    # Now update status using our new model
    updated_payload = {"status": True}
    response = client.patch(f"/task/status?id={task_id}", json=updated_payload, headers=headers)
    assert response.status_code == 200, response.text
    updated_task = response.json()
    assert updated_task["status"] is True


def test_update_deadline():
    headers = get_auth_header("taskuser", "taskpass")
    now = datetime.now().isoformat()
    task_payload = {
        "title": "Deadline Task",
        "description": "Old description",
        "status": False,
        "created_at": now,
        "updated_at": now,
        "deadline": now
    }
    response = client.post("/task/", json=task_payload, headers=headers)
    task = response.json()["task"]
    task_id = task["task_id"]
    time.sleep(1)
    updated_deadline = datetime.now().isoformat()
    updated_payload = {"deadline": updated_deadline}
    response = client.patch(f"/task/deadline?id={task_id}", json=updated_payload, headers=headers)
    assert response.status_code == 200, response.text
    updated_task = response.json()
    updated_deadline=datetime.fromisoformat(updated_deadline).replace(second=0,microsecond=0)
    deadline=datetime.fromisoformat(updated_task["deadline"]).replace(second=0,microsecond=0)
    assert deadline == updated_deadline


def test_delete_task():
    headers = get_auth_header("taskuser", "taskpass")
    now = datetime.now().isoformat()
    task_payload = {
        "title": "Delete Task",
        "description": "To be deleted",
        "status": False,
        "created_at": now,
        "updated_at": now,
        "deadline": now
    }
    response = client.post("/task/", json=task_payload, headers=headers)
    task = response.json()["task"]
    task_id = task["task_id"]
    response = client.delete(f"/task/?id={task_id}", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "Task deleted successfully"
