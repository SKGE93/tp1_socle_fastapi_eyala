import json
import pytest

from app.factories.users_factory import UsersFactory


def test_should_return_users_given_json_with_users_key(tmp_path):
    # Arrange
    payload = {
        "users": [
            {"id": 1, "login": "alice", "age": 22},
            {"id": 2, "login": "bob", "age": 25},
        ]
    }
    p = tmp_path / "users.json"
    p.write_text(json.dumps(payload), encoding="utf-8")

    factory = UsersFactory()

    # Act
    users = factory.create_users(str(p))

    # Assert (1 assertion métier)
    assert len(users) == 2


def test_should_raise_value_error_given_json_without_users_key(tmp_path):
    # Arrange
    payload = {"items": []}
    p = tmp_path / "users.json"
    p.write_text(json.dumps(payload), encoding="utf-8")

    factory = UsersFactory()

    # Act / Assert
    with pytest.raises(ValueError, match="No users found"):
        factory.create_users(str(p))