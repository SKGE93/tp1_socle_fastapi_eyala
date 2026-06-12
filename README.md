# 🚀 TP Socle FastAPI — Gestion d'utilisateurs

> API REST de gestion d'utilisateurs construite **étape par étape** dans le cadre des TP FastAPI,
> avec une architecture en couches propre (Router → Service → Repository → ORM) et une suite de tests complète.

**Auteur : Seraphin Eyala**

---

## 📌 Présentation

Ce projet est un **socle d'API REST** développé avec FastAPI. Il part d'un simple `main.py` et évolue,
branche après branche, vers une application structurée et testée :

- validation automatique des données avec **Pydantic**,
- configuration centralisée avec **pydantic-settings** (fichier `.env`),
- persistance avec **SQLAlchemy 2.0** (ORM) et **SQLite**,
- **architecture en couches** respectant le principe d'inversion de dépendances (DIP),
- tests unitaires, d'intégration et **end-to-end** avec **pytest**.

## 🛠️ Stack technique

| Outil | Rôle |
|---|---|
| **FastAPI** | Framework web (routes, validation, OpenAPI/Swagger) |
| **Pydantic / pydantic-settings** | Modèles de données typés + configuration `.env` |
| **SQLAlchemy 2.0** | ORM — mapping objets Python ↔ tables SQL |
| **SQLite** | Base de données légère (fichier `data/app.db`) |
| **pytest** | Tests unitaires, d'intégration et e2e |
| **Uvicorn** | Serveur ASGI |

## 🏗️ Architecture

L'application suit une architecture en couches : chaque couche ne connaît que celle du dessous,
et la couche métier ne dépend **jamais** de l'infrastructure (DIP).

```
HTTP (client)
   │
   ▼
Router (FastAPI)        → reçoit la requête, valide avec Pydantic, appelle le Service
   │
   ▼
Service                 → logique métier pure (aucun import FastAPI / SQLAlchemy)
   │
   ▼
Repository (interface)  → IUsersRepository : contrat injecté dans le Service
   ├── FakeRepository   → implémentation en mémoire (tests, profil "fake")
   └── SqlRepository    → implémentation SQLAlchemy (db.add / commit / rollback)
         │
         ▼
Session SQLAlchemy      → transactions (commit / rollback), identity map
         │
         ▼
Engine                  → pool de connexions, connaît l'URL de la BDD
         │
         ▼
SQLite                  → stockage physique des données
```

**Points clés du design :**

- **`UserModel` (Pydantic) ≠ `UserTable` (ORM)** : le modèle Pydantic circule entre les couches et
  est sérialisable en JSON ; le modèle ORM est lié à SQLAlchemy et ne doit jamais être exposé dans les routes.
- **Injection de dépendances** : la session BDD est injectée via `Depends(get_db)` — un générateur
  avec `yield` qui garantit la fermeture de la session même en cas d'erreur.
- **DIP** : le Service dépend d'une interface (`IUsersRepository`), ce qui permet d'injecter un
  `FakeRepository` en test et le `SqlRepository` en production sans changer une ligne du Service.
- **Gestion des erreurs** : un doublon sur un login unique lève une `IntegrityError`, gérée dans le
  Repository avec `rollback()` et traduite en **HTTP 409 Conflict**.

## 📂 Structure du projet

```
tp1_socle_fastapi_Seraphin/
├── app/
│   ├── main.py                  # Point d'entrée FastAPI
│   ├── api/
│   │   ├── dependencies.py      # Injection de dépendances (get_db, get_service…)
│   │   └── routers/
│   │       └── users_router.py  # Routes /users
│   ├── core/
│   │   └── settings.py          # Configuration centralisée (pydantic-settings + .env)
│   ├── models/                  # Modèles Pydantic (UserModel, UserModelCreate)
│   ├── models_orm/              # Modèles SQLAlchemy (UserTable)
│   ├── db/
│   │   ├── base.py              # DeclarativeBase (registre des tables)
│   │   ├── engine.py            # Engine (pool de connexions)
│   │   └── session.py           # sessionmaker + get_db (yield)
│   ├── factories/               # UsersFactory (chargement JSON → modèles)
│   ├── repositories/
│   │   ├── protocols/           # IUsersRepository (interface)
│   │   ├── users_repository_fake.py
│   │   └── users_repository_sql.py
│   ├── services/
│   │   └── users_service.py     # Logique métier
│   └── scripts/
│       └── seed_users.py        # Peuplement initial de la BDD
├── data/
│   ├── users.json               # Données sources
│   └── app.db                   # Base SQLite
├── tests/                       # Tests organisés par étapes (step_01 → step_10)
└── requirements.txt
```

## ⚡ Démarrage rapide

```bash
# 1. Cloner le repo et se placer sur la branche la plus aboutie
git clone https://github.com/SKGE93/tp1_socle_fastapi_Eyala.git
cd tp1_socle_fastapi_Eyala
git checkout projet_fastapi_tp2_partie_11
cd tp1_socle_fastapi_Seraphin

# 2. Créer un environnement virtuel et installer les dépendances
python -m venv .venv
.venv\Scripts\activate        # Windows  (source .venv/bin/activate sous Linux/Mac)
pip install -r requirements.txt

# 3. Peupler la base de données
python -m app.scripts.seed_users

# 4. Lancer le serveur
uvicorn app.main:app --reload
# → Swagger disponible sur http://127.0.0.1:8000/docs

# 5. Lancer les tests
pytest
```

## 🌿 Progression par branches

Le projet a été construit de manière incrémentale : **chaque branche correspond à une étape du TP**.

### TP1 — Socle FastAPI

| Branche | Contenu |
|---|---|
| `projet_fastapi_partie_1` | Initialisation du projet, `requirements.txt` |
| `projet_fastapi_partie_2` | Premier `main.py` — Hello FastAPI |
| `projet_fastapi_partie_3` | Premières routes |
| `projet_fastapi_partie_4` | Typage et validation automatique (path params, erreurs 422) |
| `projet_fastapi_partie_5` | Modèles Pydantic (`UserModel` / `UserModelCreate`), `UsersFactory`, premiers tests |
| `projet_fastapi_partie_6` | Configuration centralisée (`Settings` + `.env`), protocole de factory |
| `projet_fastapi_partie_8` | Architecture en couches : Router / Service / Protocols, `.gitignore` |

### TP2 — Persistance SQLAlchemy

| Branche | Contenu |
|---|---|
| `projet_fastapi_tp2_partie_1` | `IUsersRepository` (interface) + `FakeRepository` en mémoire |
| `projet_fastapi_tp2_partie_3` | Service branché sur le repository (DIP), tests du service |
| `projet_fastapi_tp2_partie_4` | `Engine` + `Session` SQLAlchemy, création de la BDD SQLite |
| `projet_fastapi_tp2_partie_5` | Tests de la session (transactions, commit/rollback) |
| `projet_fastapi_tp2_partie_6` | Modèle ORM `UserTable` (DeclarativeBase) |
| `projet_fastapi_tp2_partie_7` | Script de seed (`seed_users.py`) |
| `projet_fastapi_tp2_partie_8` | `SqlRepository` : persistance réelle (add/commit/rollback) |
| `projet_fastapi_tp2_partie_9` | Injection de dépendances (`dependencies.py`, `Depends(get_db)`) |
| `projet_fastapi_tp2_partie_10` | Branchement complet de l'API + tests d'intégration |
| `projet_fastapi_tp2_partie_11` | Tests **end-to-end** API ↔ SQL, fiche de révision |

> 💡 La branche la plus aboutie est **`projet_fastapi_tp2_partie_11`**.

## 🧪 Stratégie de tests

Les tests sont organisés par étapes (`tests/step_01` → `tests/step_10`) et couvrent chaque couche :

- **Unitaires** : factory (JSON valide / invalide / vide), service isolé avec un Fake (rapide, déterministe),
- **Infrastructure** : engine, session, table ORM, seed,
- **Intégration** : repository SQL sur une BDD SQLite jetable (`tmp_path` / `:memory:`) — chaque test
  repart d'une base vide, aucune pollution entre tests,
- **End-to-end** : appels HTTP complets via `TestClient` jusqu'à la base SQL.

## 📖 Concepts clés appris

- **ORM** : traduction automatique entre objets Python et tables SQL.
- **Engine vs Session** : l'Engine (singleton, bas niveau) gère le pool de connexions ;
  la Session (créée à chaque requête, haut niveau) gère les transactions et l'identity map.
- **`yield` dans `get_db`** : seul moyen d'exécuter du code *avant* (ouvrir) et *après* (fermer)
  la route, avec garantie de fermeture même en cas d'exception.
- **`scalar_one()` vs `scalar_one_or_none()`** : résultat obligatoire vs résultat optionnel.
- **`flush()` / `commit()` / `refresh()`** : envoi SQL sans validation / validation définitive / rechargement depuis la BDD.

---

*Projet réalisé dans le cadre des TP FastAPI — Seraphin Eyala.*
