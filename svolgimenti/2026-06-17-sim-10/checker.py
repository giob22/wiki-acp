import grpc
import IChecker_pb2
import IChecker_pb2_grpc

from concurrent import futures
import multiprocessing as mp

import stomp

import logging

import sys

logging.basicConfig(format="(%(asctime)s) [%(name)s]\t%(message)s",
                    level=logging.INFO)

logger = logging.getLogger("CHECKER")



class CheckerServicer(IChecker_pb2_grpc.ICheckerServicer):


    def __init__(self, max_size, soglia, conn):

        self.conn: stomp.Connection = conn

        self.temp_queue = mp.Queue(maxsize=max_size)
        self.soglia = soglia
        self.lock = mp.Lock()

    
    def stream_temp(self, request_iterator, context):

        normal = True
        for data in request_iterator:

            data: IChecker_pb2.Temperature

            temperature = data.temperature
            self.lock.acquire()
            self.temp_queue.put(temperature)

            if temperature > self.soglia:
                logger.info(f"temperatura maggiore della soglia: {temperature}")
                
                ## Qui va tutta la logica di comunicazione verso il broker
                normal = False
                self.conn.send(destination="/topic/alert", body=str(temperature))
                self.lock.release()
            
        if normal: 
            return IChecker_pb2.Ack(status="NORMAL") 
        else: 
            return IChecker_pb2.Ack(status="ALERT")

    def get_average(self, request, context: grpc.ServicerContext):
        self.lock.acquire()
        sum = 0
        n = 0

        while not self.temp_queue.empty():
            sum += self.temp_queue.get()
            n += 1

        self.lock.release()
        try:
            avg = sum/n

            return IChecker_pb2.Average(avg=avg)
        
        except Exception as e:
            context.abort(grpc.grpc.StatusCode.UNAVAILABLE, "Non è presente alcuna misura di temperatura all'interno della coda.")
        



if __name__ == "__main__":

    if len(sys.argv) != 2:
        raise Exception("Non hai inserito correttamente la soglia a linea di comando")
    

    max_size = 5
    try:
        soglia = int(sys.argv[1])
    except ValueError as e:
        print(e)
        sys.exit(-1)

    with stomp.Connection([("localhost", 61613)]) as conn:

        conn.connect(wait=True)

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        port = server.add_insecure_port("localhost:50051")

        logger.info(f"listening on localhost:{port}")

        servicer = CheckerServicer(max_size=max_size,soglia=soglia, conn=conn)

        IChecker_pb2_grpc.add_ICheckerServicer_to_server(server=server, servicer=servicer)

        server.start()
        try:
            server.wait_for_termination()
        except KeyboardInterrupt:
            logger.info("terminazione completata correttamente")


        



        





        


