#function qui parse les reponse du serveur
def parse_response(response):
  #change la réponse en byte par du text
  text_response = response.decode()
  # coupe et séparre les headers du body de la reponse du serveur
  headers, body = text_response.split("\r\n\r\n", 1) # le 1 veut dire coupe une seul fois au premier sépparateurs "\r\n\r\n" au cas ou il y en aurait d'autre dans le body
  print("=====Headers=======")
  print(headers)
  print("======Body======")
  print(body)

  #coupe les lignes du header pour récupéré la 1er
  lignes = headers.split("\r\n")
  #variable qui contient les data de la reponse serveur
  status_line = lignes[0]
  print("=====Status_line=======")
  print(status_line)

  #coupe la 1er ligne du header de la requet pour recupére le staut du code
  parts = status_line.split(" ", 2)
  status_code = parts[1]

  #renvoi et print la reponse du serveur
  print("======Reponse du serveur=======")
  print("Status code :", status_code)
  print("Headers :", headers)
  print("Body :", body)

#function qui construit la requet HTTP
