
from IStation import IStation
import threading as th
from abc import ABC, abstractmethod
import socket


def worker(conn: socket.socket, delegate: IStation):
    
    ## devo ricevere il messaggio 
    ## unmarshalling
    # elaborazione
    # marshalling
    # invio del messaggio al client

    message = conn.recv(1024).decode("utf-8")

    data = message.split('-')

    if data[0] == "rent":
        serial_number_estratto = delegate.rent()


        

        conn.send(str(serial_number_estratto).encode("utf-8"))

    elif data[0] == "return_bike":
        

        try:
            serial_number = int(data[1])
        except ValueError as e:
            print(e)
            conn.send("ERRORE: Bad Request".encode("utf-8"))
            conn.close()
            return
        ack: bool = delegate.return_bike(serial_number=serial_number)



        conn.send(str(ack).encode("utf-8"))

    ## prova a mettere else, bad request anche qui
    else:
        conn.send("ERRORE: Bad Request".encode("utf-8"))
    

    conn.close()








class SkeletonStationManager(ABC, IStation):


    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
    


    def run_skeleton(self):
        # creo la socket di ascolto

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            # bind

            sock.bind((self.ip,self.port))            

            # listen → backlog

            sock.listen(5)

            host_address = sock.getsockname()
            

            print("listening on localhost:", host_address[1])

            try:
                while True:
                    conn, addr = sock.accept()

                    print(f"serving: {addr}")

                    worker_thread = th.Thread(target=worker, args=(conn,self), daemon=False)
                    worker_thread.start()

            except KeyboardInterrupt:
                print(F"server closed")
            finally:
                sock.close()



