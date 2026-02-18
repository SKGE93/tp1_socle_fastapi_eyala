from pydantic import BaseModel, Field

class UserModelCreate(BaseModel):
    login: str = Field(min_length=3)
    age: int = Field(gt=0, lt=120)

