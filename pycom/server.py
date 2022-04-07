""" Methods used for interfacing with Avail's public server """
import socket
import ssl

__SERVER = ('50.207.77.3', 443)
__STOP_ID = b'73'

def __connect_to_server():
  global __SESSION
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    ssl_sock = ssl.wrap_socket(sock, saved_session = __SESSION)
    print('Found session\n')
  except NameError:
    ssl_sock = ssl.wrap_socket(sock)
  ssl_sock.connect(__SERVER)
  __SESSION = ssl.save_session(ssl_sock)

  return ssl_sock

# Not currently in use
# def visible_routes():
#   ssl_sock = __connect_to_server()
#   http_req = (
#     b'GET /InfoPoint/rest/routes/getvisibleroutes HTTP/1.1 \r\n'
#     b'HOST: bustracker.pvta.com \r\n'
#     b'Accept: text/json, application/json; charset=utf-8 \r\n'
#     b'Connection: close \r\n'
#     b'\r\n'
#   )
#   ssl_sock.send(http_req)

#   return ssl_sock.read()

def get_stopdepartures():
  """ Returns the raw http response from the server """
  ssl_sock = __connect_to_server()
  http_req = (
    b'GET /InfoPoint/rest/stopdepartures/get/' + __STOP_ID + b'HTTP/1.1 \r\n'
    b'HOST: bustracker.pvta.com \r\n'
    b'Accept: text/json, application/json; charset=utf-8 \r\n'
    b'Connection: close \r\n'
    b'\r\n'
  )
  ssl_sock.send(http_req)

  # Break the returned raw http into headers and response
  headers, http_response = ssl_sock.read().split(b'\r\n\r\n')

  return http_response 