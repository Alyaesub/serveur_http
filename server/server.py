import socket
import os
from utils import (
  not_found,
  bad_request_respons
  )
from handlers import (
  handle_get,
  handle_post,
  handle_put,
  handle_delete
)

# création du serveur :

# créé l'objet socket le socket_écoute sert a écouter et acceter les nouveau client
socket_ecoute = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# liaison du socket ecoute a un port
socket_ecoute.bind(("0.0.0.0", 8888))
# met le socket en ecoute en attendant les requets client
socket_ecoute.listen()

#tout ce qui concerne les requet client dans un while pour rester actife apres chaque requet
while True:
  #variable pour la gestion des erreurs si bad_request == True le programme s'arrette et donne une 404 bad Request
  bad_request = False
  # creation du socket client (chaque client a son propre socket)
  client_socket, client_address = socket_ecoute.accept()
  print("=====Adress client=======")
  print(client_address)

  #recupére les data du header en byte via tcp
  data_tcp = client_socket.recv(1024)

  #traduit les byes tcp en text
  text = data_tcp.decode()
  
  if "\r\n\r\n" not in text: #vérifie que les header sont bien fini et coup par "\r\n\r\n" pour split sinon bd request
    bad_request = True
    status, body = bad_request_respons()

  else:
    # coupe et séparre les headers du body de la requet client
    headers, request_body = text.split("\r\n\r\n", 1) # le 1 veut dire coupe une seul fois au premier sépparateurs "\r\n\r\n" au cas ou il y en aurait d'autre dans le body
    print("=====Headers=======")
    print(headers)
    print("======Request_body======")
    print(request_body)

    #coupe les lignes du header pour récupéré celle a utiliser
    lignes = headers.split("\r\n")
    #variable qui contient les data de la requete
    request_line = lignes[0]
    print("=====Request_line=======")
    print(request_line)


    #découpe la request_line pour récupéré les valeurs method, path, version
    parts = request_line.split() # utilise les espace entre les valeurs pour les split
    #verifie qu'il y a bien les 3 valeurs et stop le programme si 404 bad request
    if len(parts) != 3:
      bad_request = True
      status, body = bad_request_respons()
    else:
      methode = parts[0]
      path = parts[1]
      version = parts[2]
      print("=====Request_line Parts=======")
      print(f"Methode ou requete :", methode)
      print(f"Chemein du fichier :", path)
      print(f"Version HTTP :", version)

  # IF pour chosir la mathode demander par le client (plus tard en switch/case)
  if bad_request:
    pass # si bad_request == True alors on saute les methode et on envoie direct la respons avec les header de la bad_request
  
  # methode GET 
  elif methode == "GET":
    status, body = handle_get(path)
  
  #methode POST qui verifi si le fichier existe qui le créé si absent et met le body en contenue
  elif methode == "POST":
    status, body = handle_post(path, request_body)
  
  #methode PUT qui met a jour le contenue de ressour.txt avec le contenu du body et si le fichier existe pas il le créé
  elif methode == "PUT":
    status, body = handle_put(path, request_body)
  
  #methode delet qui supp le fichier
  elif methode == "DELETE":
    status, body = handle_delete(path)
  
  else:
    status = "405 Method Not Allowed"
    body = b"Method Not Allowed"


  #variable qui donne le lenght du body dynamiquement
  content_length = len(body)
  #reponse htpp dunamique pour toute les reponse
  headers = (
      f"HTTP/1.1 {status}\r\n"
      f"Content-Length: {content_length}\r\n"
      "Connection: close\r\n"
      "\r\n"
  )
  print("====Headers_spec=====")
  print(headers)



  #variable qui change les headers string en bytes pour les mettre dans la response du get
  headers_bytes = headers.encode()
  #créé la réponse en bytes
  response = headers_bytes + body
  #send la response
  client_socket.sendall(response)


  client_socket.close()