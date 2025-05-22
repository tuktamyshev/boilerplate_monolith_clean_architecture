from adapters.password_hasher import PasswordHasherService
from application.interfaces.password_hasher import PasswordHasherInterface
from dishka import Provider, provide


class PasswordHasherProvider(Provider):
    password_hasher = provide(PasswordHasherService, provides=PasswordHasherInterface)
