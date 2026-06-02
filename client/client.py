import socket
from handler_client import (
  parse_response,
  build_request
)

# variable globale
HOST = "127.0.0.1"
PORT = 8888

#créé le socket coter client
socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Connexion au server via l'ip et le port
socket_client.connect((HOST, PORT))

#construit la requete HTTP
request = (
  build_request("PUT", "/file", "teste post depuis client 3")
)

print("=====Request envoyé=====")
print(request)
print("========================")

#envoie la requet en byte via TCP
socket_client.sendall(request.encode())
#attend la réponse du serveur
response = socket_client.recv(4096)

#appel de la fonction parse_response qui parse la reponse
parse_response(response)

socket_client.close()