import threading as th
from proxy_station_manager import ProxyStationManager
import random
import sys




def rider_thread(stub: ProxyStationManager):
    richiesta = random.randint(0,1)

    if richiesta == 0:
        print("RENT")

        serial_number = stub.rent()
        print("[RENT] serial_number ricevuto: ", serial_number)
    elif richiesta == 1:
        
        print("RETURN_BIKE")
        serial_number = random.randint(1,100)
        ack = stub.return_bike(serial_number)
        print("[RETURN_BIKE] status operazione: ", ack)



if __name__ == "__main__":

    port = int(sys.argv[1])

    stub = ProxyStationManager("localhost", port)


    threads = [th.Thread(target=rider_thread, args=(stub,)) for _ in range(10)]

    [t.start() for t in threads]

    [t.join() for t in threads]

    print("Tutti i thread hanno terminato con successo")