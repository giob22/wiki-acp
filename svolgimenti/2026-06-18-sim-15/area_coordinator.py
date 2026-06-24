import grpc
import monitoraggio_latenze_pb2
import monitoraggio_latenze_pb2_grpc

from concurrent import futures
import threading as th

import stomp

import logging

logging.basicConfig(format="(%(asctime)s)[%(name)15s] %(message)s",
                    level=logging.INFO)

logger = logging.getLogger("AREA COORDINATOR")





class AreaCoordinatorServicer(monitoraggio_latenze_pb2_grpc.MonitoraggioLatenzeServicer):

    def __init__(self, max_size):
        super().__init__()
        self.queue = []
        self.max_size = max_size
        # sincronizzazione 

        self.lock = th.Lock()
        self.cons = th.Semaphore(0)
        self.prod = th.Semaphore(self.max_size)

        ## demone consumatore in background che agisce da consumatore

        self.thread_cons = th.Thread(target=self._deamon_analyzer, args=(), daemon=True)
        self.thread_cons.start()

        # inizializzo la connessione a stomp
        self.conn = stomp.Connection([("localhost", 61613)])
        self.conn.connect(wait=True)

        logger.info("server configurato correttamente")

    def _deamon_analyzer(self):
        
        while True:

            self.cons.acquire()

            self.lock.acquire()
            latency = self.queue.pop(0)
            self.lock.release()

            self.prod.release()

            logger.info(f"latenza estratta = {latency}")

            ## Non devo gestire la concorrenza poiché è presente un unico thread che ha la possibilità di inviare
            ## frame stomp, se non fosse così allora avrei dovuto wrappare la send con un lock
            if latency > 50:
                self.conn.send(destination="/topic/ftth_alerts", body=str(latency))
            
            

        
        
    def close(self):
        self.conn.disconnect()

    def get_network_status(self, request, context):
        

        self.lock.acquire()

        elem_in_coda = len(self.queue)

        self.lock.release()

        return monitoraggio_latenze_pb2.Status(status="CONGESTION") if elem_in_coda > 3 else monitoraggio_latenze_pb2.Status(status="NOMINAL")
    
    


    
    def stream_ping(self, request_iterator, context):
        numero_pacchetti_accodati = 0
        for request in request_iterator:
            numero_pacchetti_accodati += 1
            request: monitoraggio_latenze_pb2.Ping
            self.prod.acquire()

            self.lock.acquire()
            self.queue.append(request.latency)
            self.lock.release()

            self.cons.release()

        return monitoraggio_latenze_pb2.PingReply(pkt_rcvd=numero_pacchetti_accodati)
    



if __name__ == "__main__":

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    servicer = AreaCoordinatorServicer(5)
    monitoraggio_latenze_pb2_grpc.add_MonitoraggioLatenzeServicer_to_server(server=server,servicer=servicer)

    listening_port = server.add_insecure_port("localhost:50051")

    logger.info(f"listening on localhost:{listening_port}")

    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        servicer.close()


        
