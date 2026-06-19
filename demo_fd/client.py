import socket
import sys

porta = int(sys.argv[1]) if len(sys.argv) > 1 else 9000
host = '127.0.0.1'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, porta))
print(f"[CLIENT] connesso a {host}:{porta}, fd locale={s.fileno()}")

s.sendall(b"ciao dal client")
risposta = s.recv(1024)
print(f"[CLIENT] risposta: {risposta!r}")
s.close()
