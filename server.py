import socket

# créé l'objet socket le socket_écoute sert a écouter et acceter les nouveau client
socket_ecoute = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# liaison du socket ecoute a un port
socket_ecoute.bind(("0.0.0.0", 8888))

# met le socket en ecoute en attendant les requets client
socket_ecoute.listen()

# creation du socket client (chaque client a son propre socket)
client_socket, client_address = socket_ecoute.accept()
print(client_address)

#recupére les data du header en byte via tcp
data_tcp = client_socket.recv(1024)
print(data_tcp)

#traduit les byes tcp en text
text = data_tcp.decode()
print(text)

# coupe et séparre les headers du body
headers, body = text.split("\r\n\r\n", 1) # le 1 veut dire coupe une seul fois au premier sépparateurs "\r\n\r\n" au cas ou il y en aurait d'autre dans le body
print(headers)
print(body)

#coupe les lignes du header pour récupéré celle a utiliser
lignes = headers.split("\r\n")
#variable qui contient les data de la requete
request_line = lignes[0]
print(request_line)

#découpe la request_line pour récupéré les valeurs method, path, version
parts = request_line.split() # utilise les espace entre les valeurs pour les split
#verifie qu'il y a bien les 3 valeurs
if len(parts) != 3:
  print("Erreur lors de la lecture des headers")
else:
  methode = parts[0]
  path = parts[1]
  version = parts[2]
  print(f"Methode ou requete :", methode)
  print(f"Chemein du fichier :", path)
  print(f"Version HTTP :", version)

""" response = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Length: 2\r\n"
    "Connection: close\r\n"
    "\r\n"
    "OK"
)

client_socket.sendall(response.encode()) """


client_socket.close()