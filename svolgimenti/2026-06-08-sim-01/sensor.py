from monitor_proxy import MonitorSensorProxy
import sys
import random
import threading as th
import time 

LOCATIONS = ["sala", "cucina", "bagno"]
N_REQUESTS_PER_THREAD = 4
N_THREAD = 3

def sensor(proxy: MonitorSensorProxy):
    for i in range(N_REQUESTS_PER_THREAD):
        location = random.choice(LOCATIONS)
        temperature = round(random.uniform(15,35), 1)
        proxy.send_reading(location, temperature)
        time.sleep(1)


if __name__ == "__main__":
    port = int(sys.argv[1])

    proxy = MonitorSensorProxy(ip="localhost", port=port)

    threads = [th.Thread(target=sensor, args=(proxy,))for _ in range(N_THREAD)]

    [x.start() for x in threads]

    [x.join() for x in threads]


