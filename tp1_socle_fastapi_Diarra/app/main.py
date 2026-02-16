from fastapi import FastAPI
from pydantic import BaseModel, Field
from app.factories.users_factory import create_users
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
    json_users = create_users()
    return json_users

@app.get("/users/{user_id}")
def get_user(user_id : int):
    return {"id": user_id}


