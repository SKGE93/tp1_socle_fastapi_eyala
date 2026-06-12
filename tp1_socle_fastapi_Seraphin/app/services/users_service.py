from typing import List, Optional
from app.models.user_model import UserModel
from app.models.user_model_create import UserModelCreate
from app.services.users_service_protocol import IUsersService
from app.factories.users_factory_protocol import IUserFactory

class UsersService:

    """
    Service applicatif : orchestre la logique Users.

    - charge les users via la factory (source JSON pour ce TP)
    - expose list/get/create
    - persistance en mémoire (volontairement simple)
    """

    def __init__(self, factory: IUserFactory, users_json_path: str):
        self.factory = factory
        self._users: list[UserModel] = factory.create_users(users_json_path)


    def create_user(self, user: UserModelCreate) -> UserModel:
        next_id = max(user.id for user in self._users) + 1

        created_user = UserModel(
            id=next_id,
            login=user.login,
            age=user.age
        )

        self._users.append(created_user)
        return created_user


    def get_user_by_id(self, user_id: int) -> Optional[UserModel]:
        for user in self._users:
            if user.id == user_id:
                return user
        return None

    def list_users(self) -> List[UserModel]:
        return list(self._users)