"""
Rôle de ce fichier de test :

Valider le comportement de FakeUsersRepository (repository en mémoire).

Objectifs pédagogiques :
- vérifier que le repository charge les données via la factory (JSON -> objets),
- valider les comportements CRUD en mémoire (list, get, create),
- garantir que le repository reste indépendant de FastAPI, Settings et DB,
- renforcer la progression : Factory -> Repository -> Service.

Règles du TP :
- pattern AAA (Arrange / Act / Assert),
- 1 test = 1 comportement,
- 1 assertion métier principale par test.
"""

import json
from pathlib import Path

from app.factories.users_factory import UsersFactory
from app.models.user_model_create import UserModelCreate
from app.repositories.users_repository_fake import FakeUsersRepository


def _write_users_json(tmp_path: Path, users_payload: list[dict]) -> Path:
    """
    Helper de test.

    Rôle :
    - créer un fichier users.json minimal dans un répertoire temporaire,
    - garantir l'indépendance des tests vis-à-vis du fichier data/users.json.

    Args:
        tmp_path (Path): répertoire temporaire pytest.
        users_payload (list[dict]): liste d'objets user au format JSON.

    Returns:
        Path: chemin du fichier JSON créé.
    """
    p = tmp_path / "users.json"
    p.write_text(json.dumps({"users": users_payload}), encoding="utf-8")
    return p


def test_should_list_users_given_repository_loaded_from_json(tmp_path):
    """
    Vérifie que list_users retourne les utilisateurs chargés depuis le JSON.
    """
    # Arrange
    p = _write_users_json(
        tmp_path,
        [
            {"id": 1, "login": "alice", "age": 20},
            {"id": 2, "login": "bob", "age": 22},
        ],
    )
    repo = FakeUsersRepository(factory=UsersFactory(), json_path=str(p))

    # Act
    users = repo.list_users()

    # Assert (1 assertion métier)
    assert len(users) == 2


def test_should_return_user_given_existing_id(tmp_path):
    """
    Vérifie que get_user_by_id renvoie un UserModel si l'id existe.
    """
    # Arrange
    p = _write_users_json(
        tmp_path,
        [
            {"id": 1, "login": "alice", "age": 20},
            {"id": 2, "login": "bob", "age": 22},
        ],
    )
    repo = FakeUsersRepository(factory=UsersFactory(), json_path=str(p))

    # Act
    user = repo.get_user_by_id(2)

    # Assert (1 assertion métier)
    assert user is not None


def test_should_return_none_given_unknown_id(tmp_path):
    """
    Vérifie que get_user_by_id renvoie None si l'id n'existe pas.
    """
    # Arrange
    p = _write_users_json(
        tmp_path,
        [
            {"id": 1, "login": "alice", "age": 20},
        ],
    )
    repo = FakeUsersRepository(factory=UsersFactory(), json_path=str(p))

    # Act
    user = repo.get_user_by_id(999)

    # Assert (1 assertion métier)
    assert user is None


def test_should_create_user_and_generate_id_given_payload(tmp_path):
    """
    Vérifie que create_user :
    - ajoute un user en mémoire
    - génère un id = max(id existants) + 1
    """
    # Arrange
    p = _write_users_json(
        tmp_path,
        [
            {"id": 10, "login": "alice", "age": 20},
        ],
    )
    repo = FakeUsersRepository(factory=UsersFactory(), json_path=str(p))
    payload = UserModelCreate(login="charlie", age=30)

    # Act
    created = repo.create_user(payload)

    # Assert (1 assertion métier)
    assert created.id == 11