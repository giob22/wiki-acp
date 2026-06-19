from skeleton_station_manager import SkeletonStationManager
import threading as th
import requests


URL = "http://localhost:5000"

class StationManagerServicer(SkeletonStationManager):


    def __init__(self, max_size, ip, port):
        super().__init__(ip, port)
        self.max_size = max_size

        self.bike_queue = []

        self.lock = th.Lock()
        self.prod = th.Condition(self.lock)
        self.cons = th.Condition(self.lock)

    def rent(self):
        
        with self.cons:

            while len(self.bike_queue) == 0:
                self.cons.wait()

            serial_number = self.bike_queue.pop(0)

            self.prod.notify()

        
        ## QUI VA LA LOGICA DI COMUNICAZIONE CON FLASK

        response = requests.post(URL + "/update_history", json={"operation": "rent", "serial_number": serial_number})

        try:
            response.raise_for_status()
            print(f"risposta del server Flask: {response.json()}")
        except requests.exceptions.HTTPError as e:
            print(e)
            


        return serial_number
    
    def return_bike(self, serial_number):


        with self.prod:
            while len(self.bike_queue) == self.max_size:
                self.prod.wait()

            self.bike_queue.append(serial_number)

            self.cons.notify()

        


        ## QUI VA LA LOGICA DI COMUNICAZIONE CON FLASK
        response: requests.Response = requests.post(URL + "/update_history", json={"operation": "return", "serial_number": serial_number})

        try:
            response.raise_for_status()
            print(f"risposta del server Flask: {response.json()}")
        except requests.exceptions.HTTPError as e:
            print(e)
            return False
        else:
            return True



    


if __name__ == "__main__":

    servicer = StationManagerServicer(5, "localhost", 0)

    servicer.run_skeleton()


        






