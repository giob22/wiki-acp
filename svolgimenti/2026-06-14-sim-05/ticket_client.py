import threading as th
from ServerProxy import ServerProxy
import sys
import random
import time
N_THREAD = 6

metodi = ["reserve", "check"]
event = ["EVT-A", "EVT-B", "EVT-C"]


def client(proxy:ServerProxy, id):
    for i in range(3):
        op = random.choices(metodi, [7,3])[0]

        if op == "reserve":
            event_id = random.choice(event)
            qty = random.randint(1,3)

            res = proxy.reserve(event_id=event_id, qty=qty)

            esito = res.split("\|")[0]
            if esito == "OK":
                print(f"[CLIENT-{id}] RESERVE {res} → RESERVED")
            else:
                print(f"[CLIENT-{id}] RESERVE {res} → NOT ENOUGH SEATS")
        else:
            event_id = random.choice(event)

            res = proxy.check(event_id=event_id)

            print(f"[CLIENT-{id}] CHECK {res} seats available")

        time.sleep(0.5)









if __name__ == "__main__":
    if not len(sys.argv) == 2: raise Exception("bad arguments")

    proxy = ServerProxy("localhost",int(sys.argv[1]))

    threads = [th.Thread(target=client, args=(proxy,id + 1), daemon=False) for id in range(N_THREAD)]

    [t.start() for t in threads]
    [t.join() for t in threads]

