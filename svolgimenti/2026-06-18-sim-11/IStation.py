from abc import ABC, abstractmethod


class IStation(ABC):

    @abstractmethod
    def rent(self) -> int:
        '''
        consumatore
        '''
        raise NotImplementedError
    

    @abstractmethod
    def return_bike(self, serial_number) -> bool:
        '''
        produttore
        '''
        raise NotImplementedError