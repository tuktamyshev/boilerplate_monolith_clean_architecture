from adapters.email_service import DevelopEmailService, EmailService
from application.interfaces.email import EmailServiceInterface
from dishka import Provider, Scope, provide


class EmailServiceProvider(Provider):
    email_service = provide(EmailService, provides=EmailServiceInterface)


class DevelopEmailServiceProvider(Provider):
    email_service = provide(DevelopEmailService, provides=EmailServiceInterface, scope=Scope.REQUEST)
