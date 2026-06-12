from __future__ import annotations

from app.factories.users_factory_protocol import IUsersFactory
from app.models.user_model import UserModel
from app.models.user_model_create import UserModelCreate


class FakeUsersRepository:
    """
    Implémentation en mémoire de IUsersRepository.
    Utilisée exclusivement dans les tests — pas de BDD, pas de SQLAlchemy.
    Charge les users initiaux via la factory (JSON), puis stocke en mémoire.
    """

    def __init__(self, factory: IUsersFactory, json_path: str) -> None:
        # Charge les users depuis le JSON via la factory, stocke en mémoire
        self._store: list[UserModel] = factory.create_users(json_path)

    def list_users(self) -> list[UserModel]:
        return list(self._store)

    def get_user_by_id(self, user_id: int) -> UserModel | None:
        return next((u for u in self._store if u.id == user_id), None)

    def create_user(self, payload: UserModelCreate) -> UserModel:
        next_id = max((u.id for u in self._store), default=0) + 1
        user = UserModel(
            id=next_id, 
            login=payload.login, 
            age=payload.age
        )
        self._store.append(user)
        return user
