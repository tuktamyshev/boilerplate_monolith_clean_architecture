from dataclasses import dataclass


@dataclass(eq=False, frozen=True)
class DomainException(Exception):
    @property
    def message(self) -> str:
        return "DomainException occurred"
