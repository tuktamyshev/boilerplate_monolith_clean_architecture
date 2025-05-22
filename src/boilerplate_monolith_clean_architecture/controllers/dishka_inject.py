from inspect import Parameter
from typing import Callable

from dishka import AsyncContainer
from dishka.integrations.base import wrap_injection


# self-written inject from dishka for controllers for which there are no integrations
def inject(func: Callable) -> Callable:
    additional_params = [
        Parameter(
            name="dishka_container",
            annotation=AsyncContainer,
            kind=Parameter.KEYWORD_ONLY,
        ),
    ]
    return wrap_injection(
        func=func,
        is_async=True,
        additional_params=additional_params,
        container_getter=lambda _, p: p["dishka_container"],
    )
