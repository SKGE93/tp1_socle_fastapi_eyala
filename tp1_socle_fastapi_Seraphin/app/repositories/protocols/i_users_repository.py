from __future__ import annotations

from typing import Protocol

from app.models.user_model import UserModel
from app.models.user_model_create import UserModelCreate


class IUsersRepository(Protocol):
    """
    Contrat d'acces au donnees utilisateur

    objectif:
    -fournir api  stable au service
    - masquer la source reelle(json, sqlite, etc...)
    - peremttre de remplacer l'infrastructure sans modifier le service ni les routes
    """

    def list_users(self) -> list[UserModel]:
        """return: liste des users"""
        ...

    def get_user_by_id(self, user_id: int) -> UserModel | None:
        """retourne un user et none si introuvable"""
        ...

    def create_user(self, payload: UserModelCreate) -> UserModel:
        """Creation d'un user et retourne l'utilisateur cree"""