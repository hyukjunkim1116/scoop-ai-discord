from pydantic import BaseModel,Field

class AIMessage(BaseModel):
    message: str = Field(description="message of assistant")
    affinity: int = Field(description="affinity of assistant. 0 to 100")
    user_id: int = Field(description="user id")
    channel_id: int = Field(description="channel id")

class UserMessage(BaseModel):
    message: str = Field(description="message of user")
    user_id: int = Field(description="user id")
    channel_id: int = Field(description="channel id")

class Character(BaseModel):
    message: str = Field(description="answer of assistant")
    affinity: int = Field(description="affinity of assistant. 0 to 100")

class User(BaseModel):
    message: str = Field(description="answer of assistant")
    affinity: int = Field(description="affinity of assistant. 0 to 100")
