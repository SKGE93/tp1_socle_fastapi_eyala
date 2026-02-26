from fastapi.testclient import TestClient
import pytest
import os
from pathlib import Path
from app.main import app
from app.db.base import Base
from app.db.engine import get_engine, _cached_engine
from app.core.settings import get_settings
from app.models_orm.user_table import UserTable
from app.scripts.seed_users import main as seed_main

@pytest.fixture(autouse=True)
def setup_sql_e2e(monkeypatch, tmp_path):
    """
    Configure l'application pour utiliser le profil SQL et une base SQLite temporaire.
    """
    # Arrange : Création d'un fichier temporaire pour la base SQLite de test
    test_db_file = tmp_path / "test_e2e.db"
    test_db_url = f"sqlite+pysqlite:///{test_db_file}"
    
    # Injection des variables d'environnement pour le profil SQL
    monkeypatch.setenv("APP_PROFILE", "sql")
    monkeypatch.setenv("DATABASE_URL", test_db_url)
    
    # Nettoyage des caches Pydantic Settings et SQLAlchemy Engine
    get_settings.cache_clear()
    _cached_engine.cache_clear()
    
    # Initialisation du schéma (création des tables)
    # On importe UserTable pour s'assurer qu'il est enregistré dans Base.metadata
    engine = get_engine(test_db_url)
    Base.metadata.create_all(bind=engine)
    
    yield
    
    # Nettoyage
    Base.metadata.drop_all(bind=engine)
    get_settings.cache_clear()
    _cached_engine.cache_clear()

def test_should_create_user_in_sql_db():
    # Arrange
    client = TestClient(app)
    payload = {"login": "john_e2e", "age": 30}
    
    # Act
    response = client.post("/users", json=payload)
    
    # Assert
    assert response.status_code == 201

def test_should_read_user_from_sql_db():
    # Arrange
    client = TestClient(app)
    # On crée d'abord un utilisateur
    payload = {"login": "alice_e2e", "age": 25}
    create_resp = client.post("/users", json=payload)
    user_id = create_resp.json()["id"]
    
    # Act
    response = client.get(f"/users/{user_id}")
    
    # Assert
    assert response.json()["login"] == "alice_e2e"

def test_should_list_all_users_from_sql_db():
    # Arrange
    client = TestClient(app)
    client.post("/users", json={"login": "user1", "age": 20})
    client.post("/users", json={"login": "user2", "age": 25})
    
    # Act
    response = client.get("/users")
    
    # Assert
    assert len(response.json()) >= 2

def test_should_return_404_status_when_user_not_found():
    # Arrange
    client = TestClient(app)
    
    # Act
    response = client.get("/users/9999")
    
    # Assert
    assert response.status_code == 404

def test_should_verify_persistence_with_seed(monkeypatch):
    # Arrange
    # On s'assure que le seed utilise le bon fichier JSON de test
    # (data/users.json existe déjà et contient des données)
    client = TestClient(app)
    seed_main() # On lance le script de seed
    
    # Act
    response = client.get("/users")
    
    # Assert
    assert len(response.json()) > 0
