import socket
import os

#variable global :

#path de la ressource
RESOURCE_PATH = "data/resource.txt"

# création du serveur :

# créé l'objet socket le socket_écoute sert a écouter et acceter les nouveau client
socket_ecoute = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# liaison du socket ecoute a un port
socket_ecoute.bind(("0.0.0.0", 8888))
# met le socket en ecoute en attendant les requets client
socket_ecoute.listen()

#tout ce qui concerne les requet client dans un while pour rester actife apres chaque requet
while True:
  # creation du socket client (chaque client a son propre socket)
  client_socket, client_address = socket_ecoute.accept()
  print(client_address)

  #recupére les data du header en byte via tcp
  data_tcp = client_socket.recv(1024)
  print(data_tcp)

  #traduit les byes tcp en text
  text = data_tcp.decode()
  print(text)

  # coupe et séparre les headers du body de la requet client
  headers, request_body = text.split("\r\n\r\n", 1) # le 1 veut dire coupe une seul fois au premier sépparateurs "\r\n\r\n" au cas ou il y en aurait d'autre dans le body
  print(headers)
  print(request_body)

  #coupe les lignes du header pour récupéré celle a utiliser
  lignes = headers.split("\r\n")
  #variable qui contient les data de la requete
  request_line = lignes[0]
  print(request_line)
  print("============")


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

  # IF pour chosir la mathode demander par le client (plus tard en switch/case)
  # methode GET 
  if methode == "GET":
    # le if qui vérifie si le fichier existe et créé les status et body encoder
    if path != "/file":
      status = "404 Not Found"
      body = b"Erreur de path"
    
    elif not os.path.isfile(RESOURCE_PATH) :
      print("============")
      status = "404 Not Found"
      body = b"fichier introuvable"
    
    else:
      status = "200 OK"
      print("============")
      print(f"{RESOURCE_PATH} existe.")
      
      f = open(RESOURCE_PATH, 'rb')
      body = f.read()
      print("============")
      print(body)
      f.close()
  
  #methode PUT qui verifi si le fichier existe qui le créé si absent et met le body en contenue
  elif methode == "POST":
    if path != "/file":
      status = "404 Not Found"
      body = b"Erreur de path"
    
    elif os.path.exists(RESOURCE_PATH) :
      print("============")
      status = "409 Conflict"
      body = b"fichier deja existant"
    
    else:
      status = "201 Created"
      print("============")
      print(f"le fichier : {RESOURCE_PATH}, a était créé avec success .")
      
      f = open(RESOURCE_PATH, 'w')
      f.write(request_body)
      print("============")
      print(request_body)
      f.close()
      body = b"created\n"
  
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
  print("=========")
  print(headers)



  #variable qui change les headers string en bytes pour les mettre dans la response du get
  headers_bytes = headers.encode()
  #créé la réponse en bytes
  response = headers_bytes + body
  #send la response
  client_socket.sendall(response)


  client_socket.close()