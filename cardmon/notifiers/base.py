from abc import ABC, abstractmethod

class BaseNotifier(ABC):
    @abstractmethod
    async def send(self, results: list) -> None: pass
