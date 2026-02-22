from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base ORM SQLAlchemy (déclarative).

    Responsabilités :
    - servir de classe mère à toutes les tables ORM,
    - centraliser le metadata (tables, contraintes),
    - permettre la création du schéma (Base.metadata.create_all).

    Remarque :
    - Toutes les classes ORM doivent hériter de Base.
    """
