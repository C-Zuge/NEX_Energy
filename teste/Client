import sys
import socket
import time

IP = '127.0.0.1'
Port = 8081

print('Entre com o Numero da UC')
UC = input()

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    sock.connect((IP,Port))
    sock.send(bytes(UC,'utf-8'))
except:
    print('### Bind Error, closing session ###')
    time.sleep(2)
    sys.exit()
while True:
    print('Digite comando: ')
    com = input()
    sock.send(bytes(com,'utf-8'))
