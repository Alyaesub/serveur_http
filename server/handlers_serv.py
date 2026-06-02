import os
from utils import (
  not_found,
  bad_request_respons
  )

#path de la ressource
RESOURCE_PATH = "server/data/resource.txt"

# methode GET 
def handle_get(path):
  # le if qui vérifie si le fichier existe et créé les status et body encoder
    if path != "/file":
      status, body = not_found() #appel de la fonction
    
    elif not os.path.isfile(RESOURCE_PATH) :
      status = "404 Not Found"
      body = b"fichier introuvable"
    
    else:
      status = "200 OK"
      print("============")
      print("============")
      print(f"{RESOURCE_PATH} existe.")
      
      f = open(RESOURCE_PATH, 'rb')
      body = f.read()
      print("============")
      print(body)
      f.close()
    
    return status, body

#methode POST qui verifi si le fichier existe qui le créé si absent et met le body en contenue
def handle_post(path, request_body):
  if path != "/file":
    status, body = not_found()
    
  elif request_body == "": #empeche la requet avec un body vide
    status, body = bad_request_respons() #appel de la function bad request
    
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
    print("======Request_body POST======")
    print(request_body)
    f.close()
    body = b"created\n"
  
  return status, body

#methode PUT qui met a jour le contenue de ressour.txt avec le contenu du body et si le fichier existe pas il le créé
def handle_put(path, request_body):
  if path != "/file":
      status, body = not_found()

  elif request_body == "": #empeche la requet avec un body vide
      status = "400 Bad Request"
      body = b"Bad Request, aucune ressource\n"
    
  elif os.path.isfile(RESOURCE_PATH) :#si le fichier exoste jiste mettre a jour le body
      status = "200 OK"
      print("============")
      f = open(RESOURCE_PATH, 'w')
      f.write(request_body)
      print("======Request_body PUT======")
      print(request_body)
      f.close()
      body = b"fichier updated\n"
    
  else:#si le fichier existe pas le créé et mettre le body en content
      status = "201 Created"
      print("=====Created=======")
      print(f"le fichier : {RESOURCE_PATH}, a était créé avec success .")
      
      f = open(RESOURCE_PATH, 'w')
      f.write(request_body)
      print("=====Request_body PUT=======")
      print(request_body)
      f.close()
      body = b"created\n"
  
  return status, body

#methode delet qui supp le fichier
def handle_delete(path):
  # le if qui vérifie si le fichier existe 
  if path != "/file":
    status, body = not_found()
    
  elif not os.path.isfile(RESOURCE_PATH) :
    print("============")
    status = "404 Not Found"
    body = b"fichier introuvable"
    
  else:
    status = "200 OK"
    os.remove(RESOURCE_PATH)
    print("=====Request_delet=======")
    print(f"{RESOURCE_PATH} supprimé avec successé.")
    body = b"deleted\n"
  
  return status, body