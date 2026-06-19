import stomp
import threading as th

import time

import random

from utility import *

VEICHELS = ["V1", "V2", "V3", "V4"]
STATUS = ["active", "maintenance"]

class query_listener(stomp.ConnectionListener):

    def on_message(self, frame):

        print(f"messaggio ricevuto:\n{frame.body}")





def report_thread(ip, port):

    with stomp.Connection([(ip,port)]) as conn:

        conn.connect(wait=True)

        veicolo = random.choice(VEICHELS)
        status = random.choice(STATUS)

        message = f"REPORT-{veicolo}-{random.randint(0,100)}-{status}"

        conn.send(destination=TOPIC_REQEUST, body=message)

        print(f"REPORT inviato:\n{message}")



        





def query_thread(ip, port):

    with stomp.Connection([(ip,port)]) as conn:

        conn.connect(wait=True)

        message = f"QUERY-{random.randint(0,100)}"

        conn.send(destination=TOPIC_REQEUST, body=message)

        print(f"QUERY inviata:\n{message}")








if __name__ == "__main__":

    # creo i thread che invieranno le richieste di REPORT

    thread_report = [th.Thread(target=report_thread, args=("localhost", 61613)) for _ in range(4)]

    thread_query = [th.Thread(target=query_thread, args=("localhost", 61613)) for _ in range(2)]

    [t.start() for t in thread_report]

    [t.start() for t in thread_query]

    

    with stomp.Connection([("localhost",61613)]) as conn:

        conn.connect(wait=True)

        conn.set_listener("ListenerDurabile", query_listener())
        conn.subscribe(destination=TOPIC_RESPONSE, id=1, ack="auto")


        [t.join() for t in thread_report]
        [t.join() for t in thread_query]
        
        try:
            while True:
                time.sleep(100)
        except KeyboardInterrupt:
            print(f"Operator terminato correttamente")
            conn.unsubscribe(id=1)
            conn.disconnect()
