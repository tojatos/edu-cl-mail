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


def test_login_check_invalid_request():
    response = client.post("/api/login_check",
                           json={"usernames": "w"})
    assert response.status_code == 422


def test_login_check_invalid_credentials():
    response = client.post("/api/login_check",
                           json={"username": USERNAME, "password": "123"})
    assert response.status_code == 401


def test_login_check():
    response = client.post("/api/login_check",
                           json={"username": USERNAME, "password": PASSWORD})
    assert response.status_code == 200
    assert response.json()["authenticated"] == True


inboxes = [
    'odbiorcza',
    'nadawcza',
    'robocza',
    'usuniete',
]


def test_number_of_mails():
    responses = [client.post(f"/api/num_mails/{i}", json={"username": USERNAME, "password": PASSWORD})
                 for i in inboxes]
    assert all(r.status_code == 200 for r in responses)
    assert all(r.json()["numberOfMails"] > 0 for r in responses)


def test_number_of_mails_incorrect_inboxes():
    incorrect_inbox = 'test'
    response = client.post(f"/api/num_mails/{incorrect_inbox}", json={"username": USERNAME, "password": PASSWORD})
    assert response.status_code == 500


def test_mail_range_odbiorcza():
    """assumes you have at least 4 mails in this inbox"""
    from_ = 0
    to_ = 3
    response = client.post(f"/api/mail_range/odbiorcza/{from_}/{to_}",
                       json={"username": USERNAME, "password": PASSWORD})
    assert response.status_code == 200
    assert len(response.json()) == to_ - from_ + 1


def test_mail_range_nadawcza():
    """assumes you have at least 2 mails in this inbox"""
    from_ = 0
    to_ = 1
    response = client.post(f"/api/mail_range/nadawcza/{from_}/{to_}",
                           json={"username": USERNAME, "password": PASSWORD})
    assert response.status_code == 200
    assert len(response.json()) == to_ - from_ + 1


def test_mail_range_robocza():
    """assumes you have at least 2 mails in this inbox"""
    from_ = 0
    to_ = 1
    response = client.post(f"/api/mail_range/robocza/{from_}/{to_}",
                           json={"username": USERNAME, "password": PASSWORD})
    assert response.status_code == 200
    assert len(response.json()) == to_ - from_ + 1


def test_mail_range_usuniete():
    """assumes you have at least 1 mail in this inbox"""
    from_ = 0
    to_ = 0
    response = client.post(f"/api/mail_range/usuniete/{from_}/{to_}",
                           json={"username": USERNAME, "password": PASSWORD})
    assert response.status_code == 200
    assert len(response.json()) == to_ - from_ + 1

