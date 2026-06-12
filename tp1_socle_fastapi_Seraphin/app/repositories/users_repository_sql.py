from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.user_model import UserModel
from app.models.user_model_create import UserModelCreate
from app.models_orm.user_table import UserTable
from app.repositories.protocols.i_users_repository import IUsersRepository


class UsersRepositorySql(IUsersRepository):

    def __init__(self, db: Session) -> None:
        self.db = db  # ← Session injectée jamais créée ici

    def list_users(self) -> list[UserModel]:
        rows = self.db.query(UserTable).all()
        return [UserModel(id=r.id, login=r.login, age=r.age) for r in rows]

    def get_user_by_id(self, user_id: int) -> UserModel | None:
        row = self.db.query(UserTable).filter(UserTable.id == user_id).first()
        if row is None:
            return None
        return UserModel(id=row.id, login=row.login, age=row.age)

    def create_user(self, payload: UserModelCreate) -> UserModel:
        row = UserTable(login=payload.login, age=payload.age)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)  # ← récupère l'id auto-généré
        return UserModel(id=row.id, login=row.login, age=row.age)
