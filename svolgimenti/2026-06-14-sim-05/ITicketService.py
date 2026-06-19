from abc import ABC, abstractmethod

class ITicketService(ABC):

    
    @abstractmethod
    def reserve(self, event_id: str, qty: int):
        raise NotImplementedError
    @abstractmethod
    def check(self, event_id: str):
        raise NotImplementedError
     