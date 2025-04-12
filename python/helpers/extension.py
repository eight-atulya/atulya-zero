from abc import abstractmethod
from typing import Any
from atulya import Atulya
    
class Extension:

    def __init__(self, atulya: Atulya, *args, **kwargs):
        self.atulya = atulya
        self.kwargs = kwargs

    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        pass