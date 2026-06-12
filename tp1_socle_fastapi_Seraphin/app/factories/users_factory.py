import json
from app.models.user_model import UserModel

def create_users(file_path: str = "data/users.json"): 
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    donnee_brute = data["users"]
    typage = [UserModel(**user) for user in donnee_brute]

    if not typage: #  si pas de cle users
        raise ValueError("Aucun utilisateur trouvé")
    return typage
    


def create_user(path):
    with open(path, "w") as f:
        json.dump(users, f)
    return {"message" : "utilisateur cree"}
    