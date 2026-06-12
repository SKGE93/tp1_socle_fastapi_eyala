from __future__ import annotations

import json
from pathlib import Path

from sqlalchemy import text

from app.db.engine import get_engine


def test_should_insert_rows_given_seed_script(tmp_path: Path, monkeypatch):
    # Arrange
    # create temp json
    json_path = tmp_path / "users.json"
    json_path.write_text(
        json.dumps({"users": [{"id": 1, "login": "alice", "age": 20}, {"id": 2, "login": "bob", "age": 22}]}),
        encoding="utf-8",
    )

    # use temp sqlite file
    db_file = tmp_path / "app.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite+pysqlite:///{db_file}")
    monkeypatch.setenv("USERS_JSON_PATH", str(json_path))

    # Act
    from app.scripts.seed_users import main  # imported after env set

    main()

    # Assert (1 assertion métier)
    engine = get_engine()
    with engine.connect() as c:
        count = c.execute(text("SELECT COUNT(*) FROM users")).scalar_one()
    assert count == 2
