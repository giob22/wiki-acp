from ITicketService import ITicketService
import socket



class ServerProxy(ITicketService):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def reserve(self, event_id, qty):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            sock.connect((self.ip,self.port))
            print("Connessione stabilita")

            message = f"reserve#{event_id}#{qty}"

            sock.send(message.encode("utf-8"))

            print(f"messaggio inviato: {message}")
            res = sock.recv(1024).decode("utf-8")

            print(f"messaggio ricevuto: {res}")
            
        return res

    def check(self, event_id):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            sock.connect((self.ip,self.port))
            print("Connessione stabilita")

            message = f"check#{event_id}"

            sock.send(message.encode("utf-8"))
            print(f"messaggio inviato: {message}")

            res = sock.recv(1024).decode("utf-8")
            print(f"messaggio ricevuto: {res}")

        
        return res
        

