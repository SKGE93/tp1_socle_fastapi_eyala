from __future__ import annotations

import json
from pathlib import Path

from app.factories.users_factory_protocol import IUsersFactory
from app.models.user_model import UserModel


class UsersFactory(IUsersFactory):
    """Implémentation concrète : JSON -> list[UserModel]."""

    def create_users(self, json_path: str) -> list[UserModel]:
        data = json.loads(Path(json_path).read_text(encoding="utf-8"))

        users_payload = data.get("users")

        if users_payload is None:
            raise ValueError("No users found")

        if not isinstance(users_payload, list):
            raise ValueError("Users must be a list")

        return [UserModel(**u) for u in users_payload]