import enum


class ApplicationMode(enum.Enum):
    PRODUCTION = "production"
    STAGING = "staging"
    DEVELOPMENT = "development"


class JWTTokenType(enum.Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class WebSocketEvents(enum.Enum):
    application_error: str = "application_error"
    internal_server_error: str = "internal_server_error"

    message: str = "message"
    new_post: str = "new_post"
    notify_about_something: str = "notify_about_something"
