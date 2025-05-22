from pydantic import BaseModel


class BrokerConfig(BaseModel):
    HOST: str
    PORT: int
    UI_PORT: int

    # sending topics
    analyze_post: str = "analyze_post"
