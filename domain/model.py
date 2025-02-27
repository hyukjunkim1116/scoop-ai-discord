from pydantic import BaseModel,Field

class AIMessage(BaseModel):
    message: str = Field(description="message of assistant")
    affinity: int = Field(description="affinity of assistant. 0 to 100")

class UserMessage(BaseModel):
    message: str = Field(description="message of user")

class Character(BaseModel):
    message: str = Field(description="answer of assistant")
    affinity: int = Field(description="affinity of assistant. 0 to 100")

class User(BaseModel):
    message: str = Field(description="answer of assistant")
    affinity: int = Field(description="affinity of assistant. 0 to 100")