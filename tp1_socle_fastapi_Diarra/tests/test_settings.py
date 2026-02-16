from app.core.settings import Settings


def test_should_use_default_path_when_env_var_is_not_set(monkeypatch, tmp_path):
    # Arrange: se placer dans un dossier temporaire (sans .env)
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("USERS_JSON_PATH", raising=False)

    # Act
    settings = Settings()

    # Assert
    assert settings.users_json_path == "data/users.json"


def test_should_use_env_var_when_defined(monkeypatch, tmp_path):
    # Arrange: se placer dans un dossier temporaire (sans .env)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("USERS_JSON_PATH", "custom/users.json")

    # Act
    settings = Settings()

    # Assert
    assert settings.users_json_path == "custom/users.json"

def test_should_use_env_var_when_defined(monkeypatch, tmp_path):
    # Arrange: se placer dans un dossier temporaire (sans .env)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("USERS_JSON_PATH", "custom/users.json")

    # Act
    settings = Settings()

    # Assert
    assert settings.users_json_path == "custom/users.json"

def test_should_change_comportement_when_env_var_is_modified(monkeypatch, tmp_path):
    # Arrange: se placer dans un dossier temporaire (sans .env)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("USERS_JSON_PATH", "custom/users.json")

    # Act
    settings = Settings()

    # Assert
    assert settings.users_json_path == "custom/users.json"