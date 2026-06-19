from ISensor import ISensor
from utility import logging
from abc import ABC, abstractmethod

import socket

logger = logging.getLogger("SKELETON")
print = logger.info


class MonitorSensorSkeleton(ISensor, ABC):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
    
    @abstractmethod
    def send_reading(self, location, temperature):
        return super().send_reading(location,temperature)
    
    def run_skeleton(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        with sock:
            try:
                sock.bind((self.ip,self.port))
                self.ip, self.port = sock.getsockname()
                sock.listen(5)
                
                print(f"listening on {self.ip}:{self.port}")
                while True:
                    conn, addr = sock.accept()
                    print(f"serving: {addr}")

                    message = conn.recv(1024).decode("utf-8")
                    data = message.split('-')

                    self.send_reading(data[0], float(data[1]))
                    
                    conn.send("ack".encode("utf-8"))
                    conn.close()

            except KeyboardInterrupt:
                print("server terminato con successo")




        