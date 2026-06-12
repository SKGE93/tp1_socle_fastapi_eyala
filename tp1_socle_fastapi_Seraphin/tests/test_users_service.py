from app.models.user_model import UserModel
from app.models.user_model_create import UserModelCreate
from app.services.users_service import UsersService


class FakeFactory:
    def __init__(self, users: list[UserModel]) -> None:
        self._users = users

    def create_users(self, json_path: str) -> list[UserModel]:
        # ignore json_path (fake)
        return list(self._users)


def test_should_list_users_given_initial_users():
    # Arrange
    factory = FakeFactory([
        UserModel(id=1, login="alice", age=22),
        UserModel(id=2, login="bob", age=25),
    ])
    service = UsersService(factory=factory, users_json_path="ignored.json")

    # Act
    users = service.list_users()

    # Assert (1 assertion métier)
    assert len(users) == 2


def test_should_return_user_given_existing_id():
    # Arrange
    factory = FakeFactory([
        UserModel(id=1, login="alice", age=22),
    ])
    service = UsersService(factory=factory, users_json_path="ignored.json")

    # Act
    user = service.get_user_by_id(1)

    # Assert (1 assertion métier)
    assert user is not None


def test_should_return_none_given_unknown_id():
    # Arrange
    factory = FakeFactory([
        UserModel(id=1, login="alice", age=22),
    ])
    service = UsersService(factory=factory, users_json_path="ignored.json")

    # Act
    user = service.get_user_by_id(999)

    # Assert (1 assertion métier)
    assert user is None


def test_should_create_user_with_incremented_id_given_payload():
    # Arrange
    factory = FakeFactory([
        UserModel(id=1, login="alice", age=22),
        UserModel(id=2, login="bob", age=25),
    ])
    service = UsersService(factory=factory, users_json_path="ignored.json")
    payload = UserModelCreate(login="charlie", age=20)

    # Act
    created = service.create_user(payload)

    # Assert (1 assertion métier)
    assert created.id == 3