import sys
from pathlib import Path

# it is necessary when starting alembic so that it can import from modules to src
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))
from adapters.orm.base import BaseORM
from adapters.orm.post import PostORM
from adapters.orm.user import UserORM

# Don't forget to mention the models here so that alembic can see them
__all__ = [
    "BaseORM",
    "PostORM",
    "UserORM",
]
