import grpc
import ICollector_pb2
import ICollector_pb2_grpc

import sys

from utility import logging

import random
import time

logger = logging.getLogger("Telematry_Probe")

N_MEASUREMENT = 10

SENSORS = ["sensor-A", "sensor-B", "sensor-C"]

if __name__ == "__main__":

    if not (1 < len(sys.argv) < 3):
        logger.error(f"Errore: non hai inserito correttamente i parametri dalla command line")
        sys.exit(-1)


    grpc_port = sys.argv[1]

    with grpc.insecure_channel(f"localhost:{grpc_port}") as channel:

        # creo lo stub 

        stub = ICollector_pb2_grpc.ICollectorStub(channel=channel)

        for _ in range(N_MEASUREMENT):
            device_id = random.choice(SENSORS)
            value = round(random.uniform(0,100),1)
            response: ICollector_pb2.Ack = stub.SendMeasurement(ICollector_pb2.Measurement(device_id=device_id, value=value))
            print(f"[SENT] device_id={device_id:<15} | response={response.status:<6}")

            time.sleep(1)



        
        