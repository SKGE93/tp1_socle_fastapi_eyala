from typing import List
from app.models.user_model import UserModel
from app.models.user_model_create import UserModelCreate
from app.repositories.protocols.i_users_repository import IUsersRepository

class UsersService:

    """
    Service applicatif : orchestre la logique Users.

    - charge les users via la factory (source JSON pour ce TP)
    - expose list/get/create
    - persistance en mémoire (volontairement simple)
    """

    def __init__(self, repository: IUsersRepository):
        self.repository = repository


    def create_user(self, user: UserModelCreate) -> UserModel:
        return self.repository.create_user(user)


    def get_user_by_id(self, user_id: int) -> UserModel | None:
       return self.repository.get_user_by_id(user_id)

    def list_users(self) -> List[UserModel]:
        return self.repository.list_users()