from monitor_skeleton import MonitorSensorSkeleton
import multiprocessing as mp
import requests

from utility import logging

logger = logging.getLogger("MONITOR_SENSOR")

def consumatore(coda, URL):
    logger = logging.getLogger("CONSUMATORE")
    with open(file="./readings.txt", mode='a') as file:
        while True:
            message:str = coda.get()

            logger.info(f"messaggio estratto dalla coda: {message}")

            data = message.split('-')
            body = {"location": data[0], "temperature": float(data[1])}

            try:
                logger.info(f"invio al server Flask il body:\n{body}")
            
                res = requests.post(url=URL+"/readings", json=body)
                data = res.json()
                res.raise_for_status()
                logging.info(f"risultato della post: {data['result']}")

                file.write(f"{message}\n")
            except requests.exceptions.JSONDecodeError as e:
                logger.info(e)
                logger.info(f"Il payload della risposta non contiene un json come ci si aspetta")
            except Exception as e:
                logger.info(f"Error: {e}")
                



        


def produttore(coda: mp.Queue, location, temperature):
    # creo il messaggio
    logger = logging.getLogger("PRODUTTORE")
    
    message = location + "-" + str(temperature)
    logger.info(f"messaggio inserito nella coda: {message}")
    
    coda.put(message)





class MonitorSensor(MonitorSensorSkeleton):

    def __init__(self, ip, port):
        super().__init__(ip, port)
        self.coda = mp.Queue() # coda process-safe su cui posso implementare il problema produttore consumatore
        cons = mp.Process(target=consumatore, args=(self.coda, "http://localhost:5000"), daemon=True)

        cons.start()
        


    def send_reading(self, location, temperature):
        prod = mp.Process(target=produttore, args=(self.coda,location, temperature))
        logger.info("avvio il produttore")
        prod.start()
        prod.join()


if __name__ == "__main__":

    server = MonitorSensor("localhost",0)
    server.run_skeleton()

        
        