#function pour la respons 404 not found
def not_found():
  return "404 Not Found", b"Erreur de path"

#function pour la respons 400 bad request
def bad_request_respons():
  return "400 Bad Request", b"Bad Request\n"