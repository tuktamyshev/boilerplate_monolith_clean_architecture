from dishka import Provider, Scope, provide

from domain.services.access import AccessService


class DomainServiceProvider(Provider):
    scope = Scope.APP

    access_service = provide(AccessService)
