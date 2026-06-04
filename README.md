# Serveur HTTP / Client HTTP TCP

Projet réalisé dans le cadre du module Réseau de la formation ZeroDay.

## Objectif

Développer un serveur HTTP et un client HTTP qui communiquent directement via des sockets TCP, sans framework.

Le but est de comprendre concrètement :

- le fonctionnement d’un serveur TCP ;
- le rôle d’un client TCP ;
- la structure d’une requête HTTP ;
- la structure d’une réponse HTTP ;
- le parsing manuel des headers et du body ;
- les méthodes HTTP utilisées pour un CRUD simple ;
- la dockerisation d’un client et d’un serveur.

---

## Architecture du projet

```txt
SERVEUR_HTTP/
├── client/
│   ├── client.py
│   └── handler_client.py
│
├── server/
│   ├── data/
│   │   └── resource.txt
│   ├── handlers_serv.py
│   ├── server.py
│   └── utils.py
│
├── Dockerfile.client
├── Dockerfile.server
├── docker-compose.yml
└── README.md
```

---

## Fonctionnement général

Le serveur écoute sur le port `8888`.

Le client se connecte au serveur via TCP, construit une requête HTTP manuellement, l’envoie au serveur, puis lit et affiche la réponse.

La ressource manipulée par le serveur est :

```txt
server/data/resource.txt
```

Le serveur gère les opérations CRUD sur cette ressource.

---

## Lancer le projet en local

### Lancer le serveur

Depuis la racine du projet :

```bash
python3 server/server.py
```

Le serveur écoute sur :

```txt
127.0.0.1:8888
```

ou :

```txt
0.0.0.0:8888
```

selon la configuration utilisée dans `server.py`.

---

## Utiliser le client en local

Depuis la racine du projet :

### GET

Lire la ressource :

```bash
python3 client/client.py get
```

### POST

Créer la ressource avec un body :

```bash
python3 client/client.py post "abc"
```

### PUT

Remplacer le contenu de la ressource :

```bash
python3 client/client.py put "nouveau contenu"
```

### DELETE

Supprimer la ressource :

```bash
python3 client/client.py delete
```

---

## Méthodes HTTP gérées

### GET

Lit le contenu de la ressource.

Réponses possibles :

```txt
200 OK
404 Not Found
```

### POST

Crée la ressource si elle n’existe pas.

Réponses possibles :

```txt
201 Created
409 Conflict
400 Bad Request
```

### PUT

Remplace le contenu de la ressource.

Réponses possibles :

```txt
200 OK
201 Created
400 Bad Request
```

### DELETE

Supprime la ressource.

Réponses possibles :

```txt
200 OK
404 Not Found
```

---

## Erreurs gérées côté serveur

Le serveur gère plusieurs erreurs HTTP.

### 400 Bad Request

Cas possibles :

- requête mal formée ;
- absence de séparation `\r\n\r\n` ;
- Request-Line invalide ;
- body absent sur POST ou PUT.

### 404 Not Found

Cas possibles :

- mauvais path ;
- fichier absent.

### 405 Method Not Allowed

Cas possible :

- méthode HTTP non supportée.

### 409 Conflict

Cas possible :

- POST sur une ressource qui existe déjà.

---

## Affichage côté client

Le client affiche au minimum :

- la requête envoyée ;
- le status code ;
- les headers reçus ;
- le body de la réponse.

Exemple :

```txt
=====Request envoyée=====
GET /file HTTP/1.1
Host: localhost
Connection: close

=====Headers=====
HTTP/1.1 200 OK
Content-Length: 3
Connection: close

=====Body=====
abc

=====Status_line=====
HTTP/1.1 200 OK

=====Reponse du serveur=====
Status code : 200
Headers : HTTP/1.1 200 OK
Content-Length: 3
Connection: close
Body : abc
```

---

## Dockerisation

Le projet peut être lancé avec Docker Compose.

### Construire les images

Depuis la racine du projet :

```bash
docker compose build
```

### Lancer le serveur

```bash
docker compose up server
```

Le serveur est lancé dans un conteneur et écoute sur le port `8888`.

Le port est exposé sur l’hôte avec :

```txt
8888:8888
```

### Lancer le client avec Docker

Dans un autre terminal :

```bash
docker compose run --rm client get
```

```bash
docker compose run --rm client post "abc"
```

```bash
docker compose run --rm client put "nouveau contenu"
```

```bash
docker compose run --rm client delete
```

---

## Scénarios de test

### 1. GET avant création

```bash
docker compose run --rm client get
```

Résultat attendu :

```txt
404 Not Found
```

### 2. POST avec body

```bash
docker compose run --rm client post "abc"
```

Résultat attendu :

```txt
201 Created
```

### 3. GET après POST

```bash
docker compose run --rm client get
```

Résultat attendu :

```txt
200 OK
Body: abc
```

### 4. POST une seconde fois

```bash
docker compose run --rm client post "def"
```

Résultat attendu :

```txt
409 Conflict
```

### 5. PUT pour remplacer le contenu

```bash
docker compose run --rm client put "nouveau contenu"
```

Résultat attendu :

```txt
200 OK
```

ou :

```txt
201 Created
```

si le fichier n’existait pas encore.

### 6. GET après PUT

```bash
docker compose run --rm client get
```

Résultat attendu :

```txt
200 OK
Body: nouveau contenu
```

### 7. DELETE

```bash
docker compose run --rm client delete
```

Résultat attendu :

```txt
200 OK
```

### 8. GET après DELETE

```bash
docker compose run --rm client get
```

Résultat attendu :

```txt
404 Not Found
```

---

## Notes Docker

Le serveur doit écouter sur :

```txt
0.0.0.0:8888
```

dans le conteneur.

Le client utilise une variable d’environnement pour joindre le serveur Docker :

```txt
HOST=server
PORT=8888
```

Dans Docker Compose, `server` correspond au nom du service serveur.

---

## Technologies utilisées

- Python 3
- Sockets TCP
- HTTP/1.1
- CLI avec `sys.argv`
- Docker
- Docker Compose
- Lecture et écriture de fichiers locaux

---

## Résultat

Le projet permet de tester un échange HTTP complet entre un client et un serveur construits manuellement au-dessus de TCP.
