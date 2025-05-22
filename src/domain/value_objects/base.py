from abc import ABC, abstractmethod
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from uuid import UUID

from pydantic._internal._schema_generation_shared import CallbackGetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema


class BaseValueObject(ABC):
    base_type: type

    @classmethod
    @abstractmethod
    def validate(cls, value: type) -> None: ...

    def __new__(cls, *args, **kwargs):  # noqa
        coerced = cls._coerce(*args, **kwargs)
        cls.validate(coerced)

        return coerced

    @classmethod
    def _coerce(cls, *args, **kwargs):  # noqa
        if args and isinstance(args[0], cls.base_type):
            coerced = args[0]
        else:
            coerced = cls.base_type(*args, **kwargs)

        return coerced

    def __init_subclass__(cls, **kwargs):  # noqa
        super().__init_subclass__(**kwargs)

        for base in cls.__bases__:
            if base in (cls, BaseValueObject, ABC, object):
                continue
            cls.base_type = base
            break
        else:
            raise TypeError(f"Cannot determine base type for {cls.__name__}")

    @classmethod
    def __get_pydantic_core_schema__(cls, _source: type, _handler: CallbackGetCoreSchemaHandler) -> CoreSchema:
        mapping = {
            str: core_schema.str_schema(),
            int: core_schema.int_schema(),
            float: core_schema.float_schema(),
            bool: core_schema.bool_schema(),
            bytes: core_schema.bytes_schema(),
            UUID: core_schema.uuid_schema(),
            datetime: core_schema.datetime_schema(),
            date: core_schema.date_schema(),
            time: core_schema.time_schema(),
            timedelta: core_schema.timedelta_schema(),
            Decimal: core_schema.decimal_schema(),
        }

        inner_schema = mapping.get(cls.base_type)
        if inner_schema is None:
            raise TypeError(f"Unsupported base_type: {cls.base_type}")

        return core_schema.no_info_after_validator_function(
            cls,
            inner_schema,
            serialization=core_schema.plain_serializer_function_ser_schema(lambda v: v),
        )
