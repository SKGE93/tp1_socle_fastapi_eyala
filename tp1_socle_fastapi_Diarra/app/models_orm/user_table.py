from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class UserTable(Base):
    """
    Table ORM représentant l'entité User en base.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column( unique=True, nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)