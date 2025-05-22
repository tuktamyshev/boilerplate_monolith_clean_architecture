from fastapi import FastAPI
from main.admin_panel.auth import AdminAuth
from main.admin_panel.model_views import (
    CallAdmin,
    UserAdmin,
)
from sqladmin import Admin
from sqlalchemy.ext.asyncio import AsyncEngine

__all__ = ["init_admin"]


async def init_admin(app: FastAPI) -> None:
    engine = await app.state.dishka_container.get(AsyncEngine)
    config = app.state.config.auth
    authentication_backend = AdminAuth(secret_key=config.ADMIN_PANEL_SECRET_KEY)
    admin = Admin(app, engine, authentication_backend=authentication_backend)

    admin.add_view(UserAdmin)
    admin.add_view(CallAdmin)
