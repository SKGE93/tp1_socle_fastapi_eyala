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
    
    # 1. Vérifier le profil
    profile = settings.app_profile

    # 2. Si fake : lecture JSON
    if profile == "fake":
        factory = UsersFactory()
        return FakeUsersRepository(factory, settings.users_json_path)

    # 3. Si sql : utilise la vraie DB
    if profile == "sql":
        if db is None:
            raise ValueError("La session DB est requise pour le profil SQL")
        return UsersRepositorySql(db)

    # 4. Sinon erreur
    raise ValueError(f"Profil applicatif inconnu : {profile}")


# -----------------------------------------------------------------------------
# 2. Fournisseur UNIQUE de service
# -----------------------------------------------------------------------------

def get_users_service_dep(
    db: Session = Depends(get_db),
) -> UsersService:
    """
    Dépendance FastAPI principale.
    
    Cette fonction :
    - lit les Settings
    - construit le repository
    - construit le service
    - retourne le service
    
    Important : Le router ne connaît jamais le repository.
    """
    settings = get_settings()
    
    # Construction du repository injecté
    repo = build_users_repository(settings, db=db)
    
    # Retourne le service prêt à l'emploi
    return UsersService(repo)
