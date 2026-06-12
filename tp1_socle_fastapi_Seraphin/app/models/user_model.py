from pydantic import BaseModel, Field

class UserModel(BaseModel):
    id: int = Field(gt=0)
    login: str = Field(min_length=3)
    age: int = Field(gt=0, lt=120)
