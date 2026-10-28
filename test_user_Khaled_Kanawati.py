import importlib

import pytest

from lab5_api import database


def user_data(name="Khaled Kanawati"):
    return {
        "name": name,
        "email": "khaled@example.com",
        "phone": "12345678",
        "address": "Beirut",
        "country": "Lebanon",
    }


@pytest.fixture
def db_file(tmp_path, monkeypatch):
    path = tmp_path / "database.db"
    monkeypatch.setattr(database, "DATABASE", path)
    return path


@pytest.fixture
def ready_database(db_file):
    database.create_db_table()
    return db_file


@pytest.fixture
def client(db_file):
    api = importlib.import_module("lab5_api.app")
    importlib.reload(api)
    api.app.config["TESTING"] = True
    return api.app.test_client()


def test_database_created_with_specified_users(db_file):
    assert not db_file.exists()
    importlib.reload(importlib.import_module("lab5_api.app"))
    assert db_file.exists()
    users = database.get_users()
    assert len(users) == len(database.INITIAL_USERS)
    assert [{field: user[field] for field in database.FIELDS} for user in users] == list(database.INITIAL_USERS)


def test_insert_user(ready_database):
    created = database.insert_user(user_data())
    assert created["user_id"] > 0
    assert created["name"] == "Khaled Kanawati"
    assert database.get_user_by_id(created["user_id"]) == created


def test_get_users(ready_database):
    created = database.insert_user(user_data())
    users = database.get_users()
    assert len(users) == len(database.INITIAL_USERS) + 1
    assert users[-1] == created


def test_get_users_by_id(ready_database):
    created = database.insert_user(user_data())
    assert database.get_user_by_id(created["user_id"]) == created
    assert database.get_user_by_id(9999) is None


def test_update_user(ready_database):
    created = database.insert_user(user_data())
    updated = {**created, "name": "Khaled Updated"}
    assert database.update_user(updated) == updated
    assert database.get_user_by_id(created["user_id"]) == updated


def test_delete_user(ready_database):
    created = database.insert_user(user_data())
    assert database.delete_user(created["user_id"]) is True
    assert database.get_user_by_id(created["user_id"]) is None


def test_api_get_user(client):
    response = client.get("/api/users/1")
    assert response.status_code == 200
    assert response.get_json()["name"] == database.INITIAL_USERS[0]["name"]
    missing = client.get("/api/users/9999")
    assert missing.status_code == 404
    assert missing.get_json() == {"error": "User not found"}


def test_api_add_user(client):
    uploaded = user_data()
    response = client.post("/api/users/add", json=uploaded)
    assert response.status_code == 201
    created = response.get_json()
    assert {key: created[key] for key in uploaded} == uploaded
    downloaded = client.get(f"/api/users/{created['user_id']}")
    assert downloaded.status_code == 200
    assert downloaded.get_json() == created


def test_api_update_user(client):
    uploaded = {**user_data("Khaled Updated"), "user_id": 1}
    response = client.put("/api/users/update", json=uploaded)
    assert response.status_code == 200
    assert response.get_json() == uploaded
    downloaded = client.get("/api/users/1")
    assert downloaded.status_code == 200
    assert downloaded.get_json() == uploaded


def test_api_delete_user(client):
    response = client.delete("/api/users/delete/1")
    assert response.status_code == 200
    assert response.get_json() == {"status": "User deleted successfully"}
    missing = client.get("/api/users/1")
    assert missing.status_code == 404
    assert missing.get_json() == {"error": "User not found"}

def test_api_get_users(client):
    response = client.get("/api/users")
    assert response.status_code == 200
    users = response.get_json()
    assert len(users) == len(database.INITIAL_USERS)
    assert [{field: user[field] for field in database.FIELDS} for user in users] == list(database.INITIAL_USERS)