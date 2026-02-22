# step_06

Composition / dépendances (DI)

Test fourni : `test_user_table.py`

Commande :

```bash
pytest tests_provides/step_06
```


# README — Tests du modèle ORM `UserTable` (Step 06)

## Objectif pédagogique

Ce test vérifie que la classe `UserTable` (modèle ORM SQLAlchemy) est correctement définie du point de vue structurel.

Il ne teste pas le comportement métier.  
Il teste la **structure de la table SQL**.

L’objectif est de comprendre :

- Comment SQLAlchemy représente les colonnes
- Comment vérifier qu’un champ est bien clé primaire
- Comment inspecter un modèle ORM sans requête SQL

---

## Pourquoi tester la structure ORM ?

Dans une architecture propre :

- `UserModel` (Pydantic) → modèle API
- `UserTable` (ORM) → modèle base de données

Il est important de garantir que :

- `id` est bien clé primaire
- les colonnes existent
- les types sont cohérents

Une erreur ici peut casser toute l’infrastructure SQL.

---

## Rôle de `InstrumentedAttribute`

Dans SQLAlchemy, lorsqu’on écrit :

```python
id: Mapped[int] = mapped_column(primary_key=True)
```

SQLAlchemy ne crée pas un simple attribut Python.

Il crée un objet spécial appelé :

```
InstrumentedAttribute
```

Cet objet :

- représente une colonne SQL
- permet de construire des requêtes (`UserTable.id == 1`)
- contient des métadonnées sur la colonne

---

## Pourquoi l’utiliser dans le test ?

Dans le test, on vérifie par exemple :

```python
assert isinstance(UserTable.id, InstrumentedAttribute)
```

Cela permet de s’assurer que :

- `id` est bien une colonne SQLAlchemy
- ce n’est pas un attribut Python classique

Ensuite, on inspecte la table :

```python
pk_columns = [c.name for c in UserTable.__table__.primary_key.columns]
assert "id" in pk_columns
```

Cela confirme que :

- `id` est bien déclaré comme clé primaire

---

## Ce que ce test valide réellement

Il valide que :

- la structure ORM correspond à la structure SQL attendue
- la clé primaire est correctement définie
- les colonnes sont bien enregistrées dans la metadata SQLAlchemy

Il ne valide pas :

- les requêtes SQL
- la persistance
- la logique métier

---

## Message pédagogique clé

Un modèle ORM mal défini peut :

- empêcher la création des tables
- casser les relations
- provoquer des erreurs au moment des insertions

Tester la structure ORM est une bonne pratique lorsqu’on introduit SQLAlchemy pour la première fois.

---

## Résumé

Ce test permet de comprendre :

- la différence entre attribut Python et colonne SQLAlchemy
- le rôle de `InstrumentedAttribute`
- comment inspecter un modèle ORM
- comment vérifier une clé primaire sans exécuter de requête
