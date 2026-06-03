import socket
import os
import sys
from handler_client import (
  parse_response,
  build_request
)

# variable globale
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8888))

#créé le socket coter client
socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Connexion au server via l'ip et le port
socket_client.connect((HOST, PORT))

############## gestion et commande CLI : #####################

#if qui verifie si ya bien au moins 2 argv
if len(sys.argv) < 2:
  print("Usage:")
  print("  python client.py get")
  print("  python client.py delete")
  print('  python client.py post "abc"')
  print('  python client.py put "nouveau contenu"')
  sys.exit(1)

#variable sys pour commande cli
action = sys.argv[1].lower()#arg 1 est la methode

#conditions pour les commande cli
if action == "get" or action == "delete":
  methode = action.upper()
  request = build_request(methode, "/file")
  
elif action == "post" or action == "put":
  if len(sys.argv) < 3:# verifie qu'on a bien les 3 argv
    print("Erreur: POST et PUT nécessitent un body")
    sys.exit(1)
    
  methode = action.upper()
  body = sys.argv[2] #arg 2 est le body
  request = build_request(methode, "/file", body)
  
else:
  print("Méthode non supporter")
  sys.exit(1)

###################################################

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