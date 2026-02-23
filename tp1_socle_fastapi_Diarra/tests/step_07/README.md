# step_07
Seed (création tables + remplissage)

Test fourni : `test_seed.py`

Commande :

```bash
pytest tests/step_07
```

---

## Questions de compréhension

### Où est créée la table ?

Dans la base SQLite (`data/app.db`), dont le chemin est défini par `DATABASE_URL` dans les settings.

### À quel moment est-elle créée ?

À l'appel de `Base.metadata.create_all(bind=engine)`, **avant** les insertions.  
Ce n'est pas dans la transaction `engine.begin()` — le commit de `engine.begin()` ne concerne que les `INSERT`.

### Que se passe-t-il si la table existe déjà ?

Rien. `create_all()` utilise `CREATE TABLE IF NOT EXISTS` en interne.  
La table existante n'est ni recréée, ni écrasée.

### Pourquoi le script ne doit-il pas dépendre de FastAPI ?

Par séparation des responsabilités :

- `FastAPI` = couche **web** → gère les requêtes HTTP, nécessite un serveur actif
- `seed_users.py` = couche **infra** → remplit la DB, doit pouvoir tourner **sans serveur**

Le seed doit pouvoir s'exécuter en ligne de commande, avant le démarrage de l'application,  
en CI/CD ou lors d'une migration — sans avoir besoin que FastAPI tourne.
