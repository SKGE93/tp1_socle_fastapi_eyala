from fastapi.testclient import TestClient
from app.main import app
from app.services.users_service import UsersService
from app.repositories.users_repository_fake import FakeUsersRepository
from app.api.dependencies import get_users_service_dep
from app.factories.users_factory import UsersFactory
import pytest

# Simulation d'un fichier JSON pour le FakeRepository
# (Le FakeRepository attend une Factory et un chemin JSON)

def override_users_service():
    factory = UsersFactory()
    repo = FakeUsersRepository(factory=factory, json_path="/tmp/users_test.json")
    return UsersService(repo)

# 1. Création du TestClient
client = TestClient(app)

def test_get_users_returns_200_and_list():
    # Arrange
    app.dependency_overrides[get_users_service_dep] = override_users_service

    # Act
    response = client.get("/users")

    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    # Nettoyage
    app.dependency_overrides.clear()

def test_get_user_by_id_returns_200_when_exists():
    # Arrange
    app.dependency_overrides[get_users_service_dep] = override_users_service

    # Act
    response = client.get("/users/1")

    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == 1

    # Nettoyage
    app.dependency_overrides.clear()

def test_post_user_returns_201_when_valid():
    # Arrange
    app.dependency_overrides[get_users_service_dep] = override_users_service
    payload = {"login": "newuser", "age": 25}

    # Act
    response = client.post("/users", json=payload)

    # Assert
    assert response.status_code == 201
    assert response.json()["login"] == "newuser"

    # Nettoyage
    app.dependency_overrides.clear()