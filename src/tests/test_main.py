import os

from fastapi.testclient import TestClient
from app.main import app
from dotenv import load_dotenv

client = TestClient(app)
load_dotenv()


def get_env(key, fallback):
    try:
        return os.environ[key]
    except KeyError:
        return fallback


USERNAME = get_env('LOGIN', '')
PASSWORD = get_env('PASSWORD', '')


# def test_read_main():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Hello World"}

def test_login_check():
    response = client.post("/api/login_check",
                           json={"username": USERNAME, "password": PASSWORD})
    assert response.status_code == 200
    assert response.json() == True
