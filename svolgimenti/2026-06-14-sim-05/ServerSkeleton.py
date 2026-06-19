import socket
from ITicketService import ITicketService
from abc import ABC, abstractmethod

import threading as th

def worker(conn: socket.socket,delegate:ITicketService):

    message = conn.recv(1024).decode("utf-8")

    data = message.split("#")

    try:
        if data[0] == "reserve":
            res = delegate.reserve(data[1],int(data[2]))
        elif data[0] == "check":
            res = delegate.check(data[1])
        else:
            res = "Error"
    except IndexError as e:
        print(e)
        res = "Error"

    conn.send(res.encode("utf-8"))

    conn.close()





class ServerSkeleton(ITicketService,ABC):

    def __init__(self, ip, port):
        self.port = port
        self.ip = ip
    @abstractmethod
    def reserve(self, event_id, qty):
        return super().reserve(qty)

    @abstractmethod
    def check(self, event_id):
        return super().check()

    def run_skeleton(self):

        try:

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

                sock.bind((self.ip, self.port))

                socket_addr = sock.getsockname()

                print(f"server is listening on {socket_addr[0]}:{socket_addr[1]}")

                sock.listen(5)

                try:
                    while True:

                        conn, addr = sock.accept()

                        print(f"serving {addr}")

                        t = th.Thread(target=worker, args=(conn,self), daemon=False)

                        t.start()


                except KeyboardInterrupt:
                    print("server chiuso")

        except Exception as e:
            print(e)


    
