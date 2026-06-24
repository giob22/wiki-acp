import grpc
import monitoraggio_latenze_pb2
import monitoraggio_latenze_pb2_grpc

import threading as th
import random

import logging

logging.basicConfig(format="(%(asctime)s)[%(name)10s] %(message)s",
                    level=logging.INFO)

logger = logging.getLogger("ONT CLIENT")

N_THREAD = 8

def gen_ping():
    for _ in range(4):
        yield monitoraggio_latenze_pb2.Ping(latency=random.randint(10,100))


def ont_client(stub:monitoraggio_latenze_pb2_grpc.MonitoraggioLatenzeStub, op):

    if op == 0:

        ping_reply: monitoraggio_latenze_pb2.PingReply = stub.stream_ping(gen_ping())

        n_pkt = ping_reply.pkt_rcvd

        logger.info(f"[stream_ping] numero di pacchetti ricevuti: {n_pkt}")

    elif op == 1:

        status: monitoraggio_latenze_pb2.Status = stub.get_network_status(monitoraggio_latenze_pb2.Empty())

        logger.info(f"[get_network_status] stato della rete: {status.status}")



    

if __name__ == "__main__":

    ## creo lo stub

    with grpc.insecure_channel("localhost:50051") as channel:

        stub = monitoraggio_latenze_pb2_grpc.MonitoraggioLatenzeStub(channel)
        # creo i thread
        threads = [th.Thread(target=ont_client, args=(stub,i%2)) for i in range(N_THREAD)]

        [t.start() for t in threads]
        [t.join() for t in threads]

        logger.info(f"terminato correttamente")


