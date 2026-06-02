# Serveur HTTP / Client HTTP TCP

Projet réalisé dans le cadre du module Réseau formation ZeroDay.

## Objectif

Développer :

- un serveur HTTP
- un client HTTP

qui communiquent exclusivement via une socket TCP, sans framework.

L'objectif est de comprendre :

- TCP
- HTTP
- les sockets
- le modèle client / serveur
- le parsing manuel des requêtes et réponses HTTP

---

# Fonctionnalités

## Serveur HTTP

Le serveur gère une ressource locale :

```txt
data/resource.txt
```

et implémente les opérations CRUD.

### GET

Lecture du contenu de la ressource.

Réponse :

```http
200 OK
```

ou

```http
404 Not Found
```

---

### POST

Création de la ressource.

Réponses :

```http
201 Created
```

```http
409 Conflict
```

```http
400 Bad Request
```

---

### PUT

Mise à jour complète de la ressource.

Réponses :

```http
200 OK
```

```http
201 Created
```

```http
400 Bad Request
```

---

### DELETE

Suppression de la ressource.

Réponses :

```http
200 OK
```

```http
404 Not Found
```

---

# Gestion des erreurs

Le serveur gère notamment :

```http
400 Bad Request
```

- requête HTTP invalide
- body absent sur POST / PUT
- Request-Line invalide

```http

404 Not Found
```

- mauvais path
- ressource absente

```http
405 Method Not Allowed
```

- méthode non supportée

```http
409 Conflict
```

- POST sur une ressource déjà existante

---

### server.py

Responsable de :

- la création du serveur TCP
- l'écoute des connexions
- la réception des requêtes
- le parsing HTTP
- le dispatch des méthodes HTTP

### handlers.py

Contient les handlers :

```python
handle_get()
handle_post()
handle_put()
handle_delete()
```

Responsables de la logique CRUD.

### utils.py

Fonctions utilitaires :

```python
not_found()
bad_request_response()
...
```

### data/

Contient la ressource manipulée par le serveur :

```
resource.txt
```

---

# Technologies utilisées

- Python 3
- Sockets TCP
- HTTP 1.1
- Manipulation de fichiers locaux

---
