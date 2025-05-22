from dataclasses import dataclass


@dataclass(eq=False, frozen=True)
class ApplicationException(Exception):
    @property
    def message(self) -> str:
        return "ApplicationException occurred"
