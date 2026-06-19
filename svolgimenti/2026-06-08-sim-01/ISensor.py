from abc import ABC, abstractmethod

class ISensor(ABC):
    @abstractmethod
    def send_reading(self, location: str, temperature: float):
        raise NotImplementedError
    
