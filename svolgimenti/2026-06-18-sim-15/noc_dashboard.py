import stomp
import multiprocessing as mp
from stomp.utils import Frame

import time

import logging

logging.basicConfig(format="(%(asctime)s)[%(name)10s] %(message)s",
                    level=logging.INFO)

logger = logging.getLogger("NOC DASHBOARD")






class MyListener(stomp.ConnectionListener):
    def on_message(self, frame: Frame):
        p = mp.Process(target=worker, args=(int(frame.body),))
        p.start()
        

def worker(latency):
    logger.info("AVVISO: DEGRADO PRESTAZIONALE")

    with open("./outges.txt", mode="a") as file:
        file.write(f"Latenza critica rilevata: {latency:<4}\n")


if __name__ == "__main__":

    with stomp.Connection([("localhost",61613)]) as conn:

        conn.connect(wait=True)

        conn.set_listener("listener", MyListener())
        
        conn.subscribe(destination="/topic/ftth_alerts", id=1, ack="auto")

        logger.info(f"listener avviato")

        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            logger.info("terminazione completata correttamente")
        finally:
            conn.remove_listener("listener")
            conn.unsubscribe(id=1)
            conn.disconnect()

