import stomp
import multiprocessing



import time

import logging

logging.basicConfig(format="(%(asctime)s) [%(name)s]\t%(message)s",
                    level=logging.INFO)

logger = logging.getLogger("ALERT_DASHBOARD")






def worker(temperatura):


    logger.info(f"temperatura ricevuta = {temperatura}")

    with open("./alerts.txt", mode="a") as file:
        file.write(f"{temperatura}\n")

class AlertListener(stomp.ConnectionListener):

    def on_message(self, frame: stomp.utils.Frame):

        body = frame.body

        p = multiprocessing.Process(target=worker, args=(body,), daemon=True)
        p.start()

        





if __name__ == "__main__":

    with stomp.Connection([("localhost", 61613)]) as conn:

        conn.connect(wait=True)
        
        
        conn.set_listener("",AlertListener())

        conn.subscribe(destination="/topic/alert", id=1, ack="auto")

        

        try:
            while True:
                time.sleep(100)
        except KeyboardInterrupt:
            logger.info("Listener terminato correttamente")
        finally:
            conn.unsubscribe(id=1)
 
        