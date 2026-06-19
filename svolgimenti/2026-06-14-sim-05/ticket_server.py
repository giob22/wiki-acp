from ServerSkeleton import ServerSkeleton
import threading as th

import requests

URL ="http://localhost:5000"

from utility import logging

logger = logging.getLogger("TICKET_SERVER")


class TicketServer(ServerSkeleton):

    def __init__(self, ip, port):
        super().__init__(ip, port)
        self.inventory = {"EVT-A": 20, "EVT-B": 15, "EVT-C": 10}
        self.lock = th.Lock()

    def reserve(self, event_id, qty):
        
        with self.lock:
            try:
                if self.inventory[event_id] >= qty:
                    self.inventory[event_id] -= qty
                    remaining = self.inventory[event_id]
                else:
                    return "ERROR|NOT ENOUGH SEATS\n"
            except KeyError:
                return "ERROR|BAD REQUEST\n"

        response = requests.post(URL + "/sale", json={"event_id": event_id, "qty": qty})

        try:
            response.raise_for_status()
            logger.info(f"risposta ricevuta dal server flask: {response}")
        except requests.exceptions.HTTPError as e:
            logger.info(e)


        logger.info(f"RESERVE {event_id} qty={qty} → (remaining={remaining}")
        return f"OK|RESERVED {qty} for {event_id}\n"
    

    def check(self, event_id):
        
        try:
            with self.lock:
                seats = self.inventory[event_id]


            logger.info(f"CHECK {event_id} → {seats} seats")
            return f"OK|{seats}\n"
        
        except KeyError:
            return "ERROR|BAD REQUEST\n"
        
if __name__ == "__main__":

    server = TicketServer("localhost", 0)
    server.run_skeleton()
            
                




