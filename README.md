# Projet DataMedia

**DataMedia** est une APIt basée sur **FastAPI** permettant de gérer les utilisateurs, l’authentification, les trajets et d’autres entités liées à l’application Wheeltrip.
Le projet est conçu pour être conteneurisé avec Docker.

---

## Arborescence

```
.
├── Dockerfile               # Image Docker de l’API
├── requirements.txt         # Dépendances Python
├── src/                     # Code source principal de l’API
│   ├── main.py               # Point d’entrée de l’application
│   ├── api/                  # Routes (auth, users, trajets, bagages, itinéraires…)
│   ├── core/                 # Configuration
│   └── db/                   # Modèles, schémas et fonctions CRUD
├── http/                    # Fichiers de test HTTP (REST Client, VSCode, Insomnia…)
│   └── users/                # Exemples de requêtes utilisateurs
└── trajets_routes/workflows  # Workflows CI/CD (GitHub Actions)
```

---

## Prérequis

- **Python** ≥ 3.11
- **pip** ou **pipenv/poetry** pour gérer les dépendances
- **Docker** (si vous souhaitez exécuter via conteneur)

---

## Installation locale (sans Docker)

1. Cloner le dépôt et entrer dans le dossier :
   ```bash
   git clone <repo_url>
   cd DataMedia
   ```

2. Créer un environnement virtuel et installer les dépendances :
   ```bash
   python -m venv venv
   source venv/bin/activate  # sous Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Lancer le serveur :
   ```bash
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. Accéder à l’API :
   - Swagger UI → http://localhost:8000/docs
   - Redoc → http://localhost:8000/redoc

---

## Lancer avec Docker

1. Construire l’image :
   ```bash
   docker build -t datamedia-api .
   ```

2. Exécuter un conteneur :
   ```bash
   docker run -d -p 8000:8000 --name datamedia datamedia-api
   ```

3. Vérifier que l’API est disponible sur :
   - http://localhost:8000/docs

---

## Structure du code

- **`src/main.py`** : point d’entrée qui démarre FastAPI.
- **`src/api/`** : contient toutes les routes organisées par domaine :
  - `auth_routes.py` → gestion login / register / token
  - `user_routes.py` → CRUD utilisateurs
  - `trajets_routes.py` → gestion des trajets
  - `bagage_routes.py` → gestion des bagages
  - `itinerary_routes.py` → gestion des itinéraires
- **`src/db/`** :
  - `models/` → définitions des tables et collections
  - `schemas/` → schémas Pydantic pour validation
  - `crud/` → fonctions d’accès aux données (MySQL/Mongo)
- **`src/core/config.py`** : configuration globale (ex. variables d’environnement)

---

## Tests des routes

Le dossier `http/` contient des fichiers `.http` permettant de tester rapidement l’API (ex. avec l’extension **REST Client** de VSCode ou avec **Insomnia/Postman**).

Exemple :
```http
### Créer un utilisateur
POST http://localhost:8000/register
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "secret"
}
```

---

## Déploiement CI/CD

Un workflow GitHub Actions est défini dans :
```
trajets_routes/workflows/update-docker-image.yml
```

Ce fichier permet de builder et pousser automatiquement l’image Docker à chaque mise à jour (selon configuration).

---

## Commandes utiles

- **Lancer le serveur localement** :
  ```bash
  uvicorn src.main:app --reload
  ```
- **Voir les logs du conteneur Docker** :
  ```bash
  docker logs -f datamedia
  ```
- **Relancer le conteneur** :
  ```bash
  docker restart datamedia
  ```
- **Arrêter et supprimer** :
  ```bash
  docker stop datamedia && docker rm datamedia
  ```

---

## Ressources utiles

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [Docker Documentation](https://docs.docker.com/)

