from ISensor import ISensor
import socket

from utility import logging

logger = logging.getLogger("PROXY")
print = logger.info


class MonitorSensorProxy(ISensor):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def send_reading(self, location: str, temperature: float):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            # creo la connessione al server

            sock.connect((self.ip, self.port))

            # preparo il messaggio

            message = location + "-" + str(temperature)
            print(f"messaggio creato: {message}")

            sock.send(message.encode("utf-8"))
            print(f"messaggio inviato")

            # ricevo il riscontro

            ack = sock.recv(1024).decode("utf-8")
            print(f"ricevuto: {ack}")





        
        