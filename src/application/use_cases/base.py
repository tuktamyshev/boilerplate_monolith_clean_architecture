from abc import ABC, abstractmethod


class UseCase[InputDTO, OutputDTO](ABC):
    @abstractmethod
    async def __call__(self, data: InputDTO) -> OutputDTO: ...
