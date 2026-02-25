# Fiche de Révision : FastAPI, Architecture et Tests (Étapes 10 & 11)

## 1. L'Étape 10 : La couche API (`users_router.py`)

### Concept clé : La Séparation HTTP
Le router est la **seule** partie du code qui gère le protocole HTTP. 
- Il valide les entrées (via Pydantic).
- Il gère les codes de statut HTTP (200, 201, 404, 409, etc.).
- Il appelle le **Service** (et jamais le Repository ou SQLAlchemy directement).

### Injection de Dépendances avec `Depends`
On utilise `Depends(get_users_service)` dans les paramètres des fonctions du router. Cela permet de "recevoir" le service prêt à l'emploi sans savoir comment il est construit (DIP - Dependency Inversion Principle).

---

### La Hiérarchie des Tests
- **Test Unitaire :** Teste une seule "brique" (une classe ou fonction) en isolation totale.
- **Test d'Intégration :** Vérifie que deux ou plusieurs couches communiquent bien ensemble (ex: Service + Repo). On teste les "passerelles".
- **Test d'Intégration Applicative / Bout-en-bout (E2E) :** C'est ce qu'on fait avec le `TestClient`. On teste toute la chaîne de couches (Router -> Service -> Repo -> BDD). On vérifie que le puzzle complet est fonctionnel.

### Comparaison : Test Unitaire vs TestClient

| Caractéristique | Test Unitaire (Scalpel) | TestClient (Plomberie/API) |
| :--- | :--- | :--- |
| **Cible** | Une fonction ou une classe isolée (ex: Service) | Toute la chaîne (Router -> Service -> Repo) |
| **FastAPI / HTTP** | ❌ Non (Appel de fonction direct) | ✅ Oui (Simule une requête HTTP réelle) |
| **Pydantic** | ❌ Non (Pas de validation automatique) | ✅ Oui (Vérifie la validité du JSON en entrée) |
| **Status Codes** | ❌ Non | ✅ Oui (Vérifie 200, 201, 404, 422, etc.) |
| **Injection** | ❌ Non (Manuelle) | ✅ Oui (Teste le mécanisme `Depends`) |
| **But** | Tester la **logique métier** | Tester l'**intégration et le contrat API** |

### Le `TestClient` (FastAPI)
- **Simulation en mémoire :** Il permet de tester l'application sans lancer de vrai serveur (comme Uvicorn). Il communique directement avec le code en mémoire.
- **Rapidité :** Pas de sockets réseau à ouvrir, les tests sont quasi instantanés.
- **Réalisme :** On utilise une interface identique à une requête réelle (`client.get`, `client.post`).
- **Débogage facilité :** Les erreurs dans le code de l'API remontent directement dans Pytest.

### Pourquoi utiliser `dependency_overrides` ?
L'**override** de dépendance permet de contrôler ce que FastAPI injecte lors des tests. C'est un dictionnaire (`app.dependency_overrides`) où l'on remplace une fonction réelle par une version de test (Fake/Stub).

**Les 5 raisons majeures à retenir :**
1. **Isolation :** On teste uniquement la couche API sans dépendre de la vraie BDD ou du vrai Service de prod.
2. **Rapidité :** Utiliser des Fakes en mémoire est quasi instantané par rapport à une base de données sur disque.
3. **Déterminisme (Anti-pollution) :** Chaque test repart d'une base vide (ex: `sqlite :memory:`) pour éviter qu'un test n'échoue à cause des données laissées par un test précédent.
4. **Indépendance d'infrastructure :** Pas besoin d'installer un serveur de base de données complexe pour faire tourner les tests.
5. **Cas limites (Edge cases) :** Permet de forcer facilement des erreurs (ex: simuler une panne BDD ou un doublon) pour vérifier que l'API renvoie le bon code HTTP (409, 500, etc.).

### Cycle de vie d'un Override
- **Activation :** `app.dependency_overrides[get_users_service] = my_fake_service`
- **Désactivation (Crucial) :** `app.dependency_overrides.clear()`
  - *Pourquoi ?* Pour ne pas polluer les tests suivants qui pourraient ne pas avoir besoin de cet override.

---

## 3. Synthèse de l'Architecture (Flux d'une requête)

1. **Client HTTP** -> Envoie une requête (ex: POST /users).
2. **Router API** -> Reçoit la requête, valide le JSON, appelle le Service via `Depends`.
3. **Service** -> Applique la logique métier, appelle le Repository.
4. **Repository** -> Parle à la BDD via **SQLAlchemy (Session)**, convertit les objets ORM en modèles Pydantic.
5. **Base de données** -> Stocke physiquement la donnée.

## 4. Questions de Compréhension (FAQ Examen)

### Pourquoi ne pas dépendre de la vraie BDD en test d'intégration ?
1. **Performance :** La vraie BDD est lente (disque/réseau). Les tests doivent être instantanés.
2. **Déterminisme (Anti-pollution) :** Le `TestClient` avec `SQLite :memory:` garantit une base vierge pour chaque test. On évite qu'un test échoue à cause de données laissées par un autre test.
3. **Indépendance :** Permet de lancer les tests sans installer de serveur de BDD externe (parfait pour la CI/CD).

### Que prouve l'utilisation d'un Override sur l'architecture ?
L'override est la preuve matérielle que l'architecture est **bien découplée** (respect du DIP - Dependency Inversion Principle) :
- On prouve qu'on peut changer l'implémentation de la "Cave" (BDD réelle vers Fake) sans modifier une seule ligne du "Salon" (le Router).
- Cela confirme que le Router ne dépend pas d'une technologie précise, mais d'un **contrat/interface** (le Service).

### Quelle est la différence fondamentale entre Unitaire et Intégration ?
- **Unitaire :** Teste la **logique métier** interne (le calcul, l'algorithme).
- **Intégration :** Teste le **contrat de communication** (la "plomberie"). On vérifie que les données (Pydantic, JSON) passent correctement d'une couche à l'autre.
