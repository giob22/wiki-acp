import stomp
import multiprocessing as mp
from stomp.utils import Frame

import time


class TopicListener(stomp.ConnectionListener):

    def __init__(self, queue, name):
        self.name = name
        self.queue: mp.Queue = queue

    def on_message(self, frame: Frame):

        message:str = frame.body

        data = message.split("-")

        print(f"{data[0]}")

        if data[0] == "DEPLOY":
            self.queue.put(message)
            print(f"[{self.name}] è stato inserito il messaggio: {message}")
        else:
            print("STO PER ELIMINARE TUTTA LA CODA ", self.name.split('_')[0])
            while not self.queue.empty():
                message = self.queue.get()
                print(f"[{self.name}] {message}")
    

def worker_gpu(gpu_queue):
    with stomp.Connection([("localhost", 61613)], auto_content_length=False) as conn:
        conn.connect(wait=True)

        conn.subscribe(destination="/topic/gpu", id=1, ack="auto")

        conn.set_listener("GPU", TopicListener(gpu_queue, "GPU_WORKER"))

        try:
            while True:
                time.sleep(50)
               
        except Exception:
            print("GPU_LISTENER terminato")
            conn.unsubscribe(id=1)



def worker_rt(rt_queue):
    with stomp.Connection([("localhost", 61613)], auto_content_length=False) as conn:
        conn.connect(wait=True)

        conn.subscribe(destination="/topic/rt", id=1, ack="auto")

        conn.set_listener("RT", TopicListener(rt_queue, "RT_WORKER"))

        try:
            while True:
                time.sleep(50)
               
        except Exception:
            print("RT_LISTENER terminato")
            conn.unsubscribe(id=1)




if __name__ == "__main__":


    rt_queue = mp.Queue()
    gpu_queue = mp.Queue()

    t_gpu = mp.Process(target=worker_gpu, args=(gpu_queue,), daemon=True)
    t_rt = mp.Process(target=worker_rt, args=(rt_queue,), daemon=True)

    t_rt.start()
    t_gpu.start()


    t_gpu.join()
    t_rt.join()















