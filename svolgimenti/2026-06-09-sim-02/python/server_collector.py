import grpc
import ICollector_pb2
import ICollector_pb2_grpc

from concurrent import futures

import stomp

import sys

from utility import logging

logger = logging.getLogger("Collector_Server")



class CollectorServerImpl(ICollector_pb2_grpc.ICollectorServicer):

    def __init__(self, host, port, coda):
        self.coda = coda
        try:
            
            self.conn = stomp.Connection([(host,port)], auto_content_length=False)
            self.conn.connect(wait=True)

        except Exception as e:
            print(e)
            sys.exit(-1)
    def SendMeasurement(self, request: ICollector_pb2.Measurement, context: grpc.ServicerContext):
        device_id = request.device_id
        value = round(request.value,1)
        print(f"[RECV] device_id={device_id:<15} | value={value:<6}")

        ## pubblichiamo il messaggio sulla coda 

        message = device_id+"|"+str(round(value, 1))
        try:
            self.conn.send(destination=self.coda, body=message)

            logger.info(f"invio del messaggio: '{message}' avvenuto con successo")

        except Exception as e:
            print(e)
            return ICollector_pb2.Ack(status="KO")
        else:
            return ICollector_pb2.Ack(status="OK")
        

if __name__ == "__main__":

    try:

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        servicer = CollectorServerImpl("localhost", 61613, "/queue/telemetry")

        grpc_port = server.add_insecure_port("localhost:0")

        logger.info(f"listening on localhost:{grpc_port}")

        ICollector_pb2_grpc.add_ICollectorServicer_to_server(servicer=servicer, server=server)

        server.start()

        server.wait_for_termination()

    except KeyboardInterrupt:
        logger.info(f"---Collector Server terminato---")
    