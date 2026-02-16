import json
import unittest
import pytest
from pydantic import ValidationError


from app.factories.users_factory import create_users


def test_create_users_valid_data(tmp_path):

    # Arrange
    data = {
        "users": [
            {"id": 1, "login": "alice", "age": 25},
            {"id": 2, "login": "bob_le_bricoleur", "age": 40}
        ]
    }

    f = tmp_path / "users.json"
    f.write_text(json.dumps(data), encoding="utf-8")

    # Act
    users = create_users(f)

    # Assert
    assert len(users) == 2
    assert users[0].login == "alice"
    assert users[1].age == 40
    assert users[0].id == 1


def test_create_users_missing_key_raises_value_error(tmp_path):

    # Arrange
    data = {"userss": []}

    f = tmp_path / "users.json"
    f.write_text(json.dumps(data), encoding="utf-8")

    # Act / Assert
    with pytest.raises(KeyError):
        create_users(f)


def test_create_users_invalid_model_raises_validation_error(tmp_path):

    # Arrange
    data = {
        "users": [
            {"id": 1, "login": "bo", "age": 200}
            # "bo" < 3 characters et l'age 200 > 120
        ]
    }

    f = tmp_path / "users.json"
    f.write_text(json.dumps(data), encoding="utf-8")

    # Act / Assert
    with pytest.raises(ValidationError):
        create_users(f)
