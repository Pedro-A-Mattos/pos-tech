import pytest
from src.auth.check_users import check_user
from src.utils.model import UserLoginSchema

def test_check_user_valid_user(monkeypatch):
    # Arrange
    test_data = UserLoginSchema(email="test@example.com", password="password123")

    # Mocking the users data using monkeypatch
    mock_users = [
        {"email": "test@example.com", "password": "password123"},
        {"email": "otheruser@example.com", "password": "password456"}
    ]
    monkeypatch.setattr("src.auth.check_users.users", mock_users)

    # Act
    result = check_user(test_data) 

    # Assert
    assert result is True

def test_check_user_invalid_user(monkeypatch):
    # Arrange
    test_data = UserLoginSchema(email="invalid@example.com", password="wrongpassword")

    # Mocking the users data using monkeypatch
    mock_users = [
        {"email": "test@example.com", "password": "password123"},
        {"email": "otheruser@example.com", "password": "password456"}
    ]
    monkeypatch.setattr("src.auth.check_users.users", mock_users)

    # Act
    result = check_user(test_data)

    # Assert
    assert result is False

def test_check_user_empty_users_list(monkeypatch):
    # Arrange
    test_data = UserLoginSchema(email="test@example.com", password="password123")

    # Mocking an empty users list using monkeypatch
    monkeypatch.setattr("src.auth.check_users.users", [])

    # Act
    result = check_user(test_data)

    # Assert
    assert result is False
