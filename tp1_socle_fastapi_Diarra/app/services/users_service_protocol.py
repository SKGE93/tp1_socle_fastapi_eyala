from typing import Protocol, List, Optional
from app.models.user_model import UserModel
from app.models.user_model_create import UserModelCreate

class IUsersService(Protocol):
    
    def list_users(self) -> list[UserModel]

    def get_user_by_id(self, user_id: int) -> Optional[UserModel]

    def create_user(self, user: UserModelCreate) -> UserModel

    