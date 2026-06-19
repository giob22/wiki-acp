from IStation import IStation
import socket


class ProxyStationManager(IStation):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        print(f"stub inizializzato")

    

    def rent(self):
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            sock.connect((self.ip,self.port))

            # marshalling del messaggio

            message = "rent-"


            sock.send(message.encode("utf-8"))

            response = sock.recv(1024).decode("utf-8")

            print(f"serial_number della bici restituita: {response}")

            if not response.lstrip("-").isdigit():
                raise RuntimeError(f"risposta inattesa dal server: {response}")

            return int(response)

            
        

    def return_bike(self,serial_number):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            sock.connect((self.ip,self.port))

            # marshalling del messaggio

            message = "return_bike-" + str(serial_number)


            sock.send(message.encode("utf-8"))

            response = sock.recv(1024).decode("utf-8")

            print(f"Status dell'operazione di return_bike: {response}")

            return response == "True"
        