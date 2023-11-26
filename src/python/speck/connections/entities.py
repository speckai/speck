from abc import ABC, abstractmethod

from ..chat.entities import Messages


class IConnector(ABC):
    @abstractmethod
    def process_message(self, messages: Messages) -> str:
        pass
