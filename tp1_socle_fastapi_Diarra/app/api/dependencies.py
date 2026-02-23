from __future__ import annotations
from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.settings import get_settings, Settings
from app.db.session import get_db

from app.repositories.protocols.i_users_repository import IUsersRepository
from app.repositories.users_repository_fake import FakeUsersRepository
from app.repositories.users_repository_sql import UsersRepositorySql

from app.factories.users_factory import UsersFactory
from app.services.users_service import UsersService

# -----------------------------------------------------------------------------
# 1. Factory de repository
# -----------------------------------------------------------------------------

def build_users_repository(
    settings: Settings,
    db: Session | None = None,
) -> IUsersRepository:
    """
    Construit le repository Users en fonction du profil applicatif.
    """
    
    # 1. Vérifier le profil (supporte app_profile ou users_backend pour les tests)
    profile = getattr(settings, "app_profile", getattr(settings, "users_backend", None))

    # 2. Si fake : lecture JSON
    if profile == "fake":
        factory = UsersFactory()
        return FakeUsersRepository(factory, settings.users_json_path)

    # 3. Si sql ou db : utilise la vraie DB
    if profile in ["sql", "db"]:
        if db is None:
            raise RuntimeError("La session DB est requise pour le profil SQL")
        return UsersRepositorySql(db)

    # 4. Sinon erreur
    raise ValueError(f"Profil applicatif inconnu : {profile}")


# -----------------------------------------------------------------------------
# 2. Fournisseur UNIQUE de service
# -----------------------------------------------------------------------------

def get_users_service(
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> UsersService:
    """
    Dépendance FastAPI principale.
    """
    # Construction du repository injecté
    repo = build_users_repository(settings, db=db)
    
    # Retourne le service prêt à l'emploi
    return UsersService(repo)

# Alias pour compatibilité avec certains tests
get_users_service_dep = get_users_service
