import grpc
import IChecker_pb2
import IChecker_pb2_grpc

import random

import logging

logging.basicConfig(format="(%(asctime)s) [%(name)s]\t%(message)s",
                    level=logging.INFO)

logger = logging.getLogger("SENSOR")


N_TEMP = 5
N_INVOCAZIONI = 5

def gen_temp():

    for _ in range(N_TEMP):
        temperature = random.randint(50,100)


        yield IChecker_pb2.Temperature(temperature=temperature)





if __name__ == "__main__":


    port = 50051

    with grpc.insecure_channel(f"localhost:{port}") as channel:

        proxy = IChecker_pb2_grpc.ICheckerStub(channel=channel)


        for _ in range(N_INVOCAZIONI):
            status: IChecker_pb2.Ack = proxy.stream_temp(gen_temp())
            logger.info(f"{status.status}")

            response: IChecker_pb2.Average = proxy.get_average(IChecker_pb2.Empty())
            logger.info(f"media={response.avg}")

    



