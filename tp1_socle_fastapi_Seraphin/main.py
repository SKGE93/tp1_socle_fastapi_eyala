from fastapi import FastAPI
from pydantic import BaseModel, Field
import json

app = FastAPI()

class User(BaseModel):
    id: int
    login: str

users = [        
        {"id": 1, "login": "alice"},
        {"id": 2, "login": "bob"},
        {"id": 3, "login": "charlie"},
        {"id": 4, "login": "diana"},
        {"id": 5, "login": "edward"},
        {"id": 6, "login": "fatima"},
        {"id": 7, "login": "guillaume"},
        {"id": 8, "login": "hana"},
        {"id": 9, "login": "ismael"},
        {"id": 10, "login": "julien"}   
        ]

@app.get("/")
def hello_fastapi():
    return{"message" : "API FastAPI opérationnelle"}

@app.get("/users",
    response_model=list[User],
    summary="recuperer la liste des utilisateurs",
    description = "retourne une liste d'utilisateur au format JSON"
)
def get_users():
    return users

@app.get("/users/{user_id}")
def get_user(user_id : int):
    json_users = UsersFactory()
    return json_users


@app.get("/search",
    summary="recuperer la liste des utilisateurs via le nom",
    description = "retourne l'utilisateur au format JSON"
)
def search(name : str | None = None):
    return {"search" : name}

class UserModelCreate(BaseModel):
    login: str = Field(min_length=3)
    age: int = Field(gt=0, lt=120)

class UserModel(BaseModel):
    id: int = Field(gt=0)
    login: str = Field(min_length=3)
    age: int = Field(gt=0, lt=120)

def UsersFactory(): 
    with open("data/users.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    donnee_brute = data["users"]
    typage = [UserModel(**user) for user in donnee_brute]
    return typage


