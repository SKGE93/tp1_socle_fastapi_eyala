import pytest
from sqlalchemy.orm import Session
from app.db.base import Base
from app.db.engine import get_engine, _cached_engine
from app.db.session import SessionLocal
from app.core.settings import get_settings

@pytest.fixture
def db(monkeypatch):
    """
    Fixture qui fournit une session SQLAlchemy pour les tests.
    Utilise une base SQLite en mémoire pour chaque test pour garantir l'isolation.
    """
    # 1. On force une URL de test (base en mémoire)
    test_db_url = "sqlite+pysqlite:///:memory:"
    monkeypatch.setenv("DATABASE_URL", test_db_url)
    
    # 2. On vide les caches pour forcer la prise en compte de l'URL de test
    get_settings.cache_clear()
    _cached_engine.cache_clear()
    
    # 3. Création du moteur et des tables (schéma de base)
    engine = get_engine(test_db_url)
    Base.metadata.create_all(bind=engine)
    
    # 4. Création de la session via ta fonction SessionLocal()
    session = SessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # On nettoie proprement après le test
        Base.metadata.drop_all(bind=engine)
