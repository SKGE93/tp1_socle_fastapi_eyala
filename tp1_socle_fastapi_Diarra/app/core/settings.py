from __future__ import annotations
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuration centralisée de l'application.

    Rôle :
    - lire automatiquement les variables d'environnement,
    - charger le fichier .env,
    - fournir des attributs typés et validés,
    - servir de point d'entrée unique pour la configuration.

    Avantage :
    - validation automatique des types,
    - documentation implicite de la configuration,
    - compatibilité production (Docker, CI/CD).
    """


    # Source de données
    app_profile:str = "fake"

    # URL de la base de données
    database_url: str = "sqlite+pysqlite:///./data/app.db"

    # Chemin vers le fichier JSON contenant les utilisateurs
    users_json_path: str = "data/users.json"

    # Optionnel : activer un mode debug (si utilisé plus tard)
    debug:bool = True

    # Optionnel : nom de l'application (si utilisé plus tard)
    app_name:str = "tp_fastapi_users"

model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Fournit une instance singleton de Settings.

    Pourquoi @lru_cache ?
    - éviter de recréer Settings à chaque injection,
    - partager la configuration dans toute l'application.

    Returns:
        Settings
    """
    return Settings()