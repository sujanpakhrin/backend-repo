from unittest.mock import MagicMock

from backend.app import app


def test_home():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json() == {
        "message": "Assignment 11 Multi-Tier Backend API"
    }


def test_get_users(mocker):
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchall.return_value = [
        {
            "id": 1,
            "name": "Sujan",
            "email": "sujan@example.com",
        },
        {
            "id": 2,
            "name": "Kenny",
            "email": "kenny@example.com",
        },
    ]

    mock_connection.cursor.return_value = mock_cursor

    mocker.patch(
        "backend.app.get_db_connection",
        return_value=mock_connection,
    )

    client = app.test_client()

    response = client.get("/api/users")

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "id": 1,
            "name": "Sujan",
            "email": "sujan@example.com",
        },
        {
            "id": 2,
            "name": "Kenny",
            "email": "kenny@example.com",
        },
    ]

    mock_cursor.execute.assert_called_once_with(
        "SELECT id, name, email FROM users"
    )


def test_create_user(mocker):
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.lastrowid = 3
    mock_connection.cursor.return_value = mock_cursor

    mocker.patch(
        "backend.app.get_db_connection",
        return_value=mock_connection,
    )

    client = app.test_client()

    response = client.post(
        "/api/users",
        json={
            "name": "Alex",
            "email": "alex@example.com",
        },
    )

    assert response.status_code == 201
    assert response.get_json() == {
        "id": 3,
        "name": "Alex",
        "email": "alex@example.com",
    }

    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        ("Alex", "alex@example.com"),
    )

    mock_connection.commit.assert_called_once()


def test_create_user_missing_fields():
    client = app.test_client()

    response = client.post(
        "/api/users",
        json={
            "name": "Alex",
        },
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "name and email are required"
    }
