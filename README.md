# Serveur HTTP / Client HTTP TCP

Projet réalisé dans le cadre du module Réseau de la formation ZeroDay.

## Objectif

Développer un serveur HTTP et un client HTTP qui communiquent directement avec des sockets TCP, sans framework.

Le but du projet est de comprendre concrètement :

- le fonctionnement d’un serveur TCP ;
- le rôle d’un client TCP ;
- la structure d’une requête HTTP ;
- la structure d’une réponse HTTP ;
- le parsing manuel des headers et du body ;
- les méthodes HTTP utilisées pour un CRUD simple.

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
└── README.md
```

---

## Fonctionnement général

Le serveur écoute sur le port `8888`.

Le client se connecte au serveur via TCP, construit une requête HTTP manuellement, l’envoie au serveur, puis lit et affiche la réponse.

Le serveur manipule une ressource locale :

```txt
server/data/resource.txt
```

---

## Lancer le serveur

Depuis la racine du projet :

```bash
python3 server/server.py
```

Le serveur écoute sur :

```txt
127.0.0.1:8888
```

En Docker, il devra écouter sur :

```txt
0.0.0.0:8888
```

---

## Utiliser le client

Depuis la racine du projet :

### GET

Lire la ressource :

```bash
python3 client/client.py get
```

### POST

Créer la ressource avec un body :

```bash
python3 client/client.py post "hello"
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

Le serveur gère plusieurs erreurs HTTP :

```txt
400 Bad Request
```

Cas possibles :

- requête mal formée ;
- absence de séparation `\r\n\r\n` ;
- Request-Line invalide ;
- body absent sur POST ou PUT.

```txt
404 Not Found
```

Cas possibles :

- mauvais path ;
- fichier absent.

```txt
405 Method Not Allowed
```

Cas possible :

- méthode HTTP non supportée.

```txt
409 Conflict
```

Cas possible :

- POST sur une ressource qui existe déjà.

---

## Affichage côté client

Le client affiche au minimum :

- le status code ;
- les headers reçus ;
- le body de la réponse.

Exemple :

```txt
Status code: 200

Headers:
HTTP/1.1 200 OK
Content-Length: 5
Connection: close

Body:
hello
```

---

## Scénarios de test

### 1. GET avant création

```bash
python3 client/client.py get
```

Résultat attendu :

```txt
404 Not Found
```

### 2. POST avec body

```bash
python3 client/client.py post "abc"
```

Résultat attendu :

```txt
201 Created
```

### 3. GET après POST

```bash
python3 client/client.py get
```

Résultat attendu :

```txt
200 OK
Body: abc
```

### 4. POST une seconde fois

```bash
python3 client/client.py post "def"
```

Résultat attendu :

```txt
409 Conflict
```

### 5. PUT pour remplacer le contenu

```bash
python3 client/client.py put "nouveau contenu"
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

### 6. DELETE

```bash
python3 client/client.py delete
```

Résultat attendu :

```txt
200 OK
```

### 7. GET après DELETE

```bash
python3 client/client.py get
```

Résultat attendu :

```txt
404 Not Found
```

---

## Technologies utilisées

- Python 3
- Sockets TCP
- HTTP/1.1
- Lecture et écriture de fichiers locaux
- CLI simple avec `sys.argv`

---

## Dockerisation

La dockerisation sera ajoutée dans une étape suivante.

Objectifs Docker :

- lancer le serveur dans un conteneur ;
- lancer le client dans un conteneur ;
- exposer le port `8888` ;
- utiliser un volume ou un dossier `/data` pour stocker la ressource ;
- permettre les tests depuis l’hôte.
