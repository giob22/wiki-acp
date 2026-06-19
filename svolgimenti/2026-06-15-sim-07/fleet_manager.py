import stomp
import time


from utility import *

import requests


class fleet_manager(stomp.ConnectionListener):


    def __init__(self, conn):
        self.conn = conn

    def on_message(self, frame: stomp.utils.Frame):

        message: str = frame.body

        data = message.split("-")
        try:

            if data[0] == "REPORT":
                payload = {"vehicle_id": data[1], "battery": int(data[2]), "status": data[3]}

                print(f"payload generato:\n{payload}")
                response = requests.post(url=URL + POST_REQUEST, json=payload)

                try:
                    response.raise_for_status()

                except requests.exceptions.HTTPError as e:
                    print(e)
                
    
    
            elif data[0] == "QUERY":
                
                threshold = data[1]
                print(f"threshold:\n{threshold}")

                response = requests.get(url=URL+GET_QUERY, params={"threshold": threshold})


                try:
                    response.raise_for_status()

                    data = str(response.json())

                    
                    
                    self.conn.send(destination=TOPIC_RESPONSE, body=data)



                except requests.exceptions.HTTPError as e:
                    print(e)

                    return "Errore: non è avvenuta correttamente la comunicazione con il server che mantiene il database"




        except Exception as e:
            print(e)
            

if __name__ == "__main__":

    ip = "localhost"
    port = 61613

    with stomp.Connection([(ip,port)]) as conn:

        conn.connect(wait=True, headers={"client-id": "fleet_manager_durable"})

        conn.subscribe(destination=TOPIC_REQEUST, id=1, ack="auto", headers={"activemq.subscriptionName": "fleet_manager"})

        conn.set_listener("ListenerDurabile", fleet_manager(conn))

        
        try:
            while True:
                time.sleep(100)
        except KeyboardInterrupt:
            print(f"server chiuso correttamente")
            conn.unsubscribe(id=1)
            conn.disconnect()


        