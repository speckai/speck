from abc import ABC, abstractmethod


class IConnector(ABC):
    @abstractmethod
    def process_message(self, message: str) -> str:
        pass
