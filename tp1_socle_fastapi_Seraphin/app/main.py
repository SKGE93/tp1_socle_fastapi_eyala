from fastapi import FastAPI
from app.api.routers import users_router

app = FastAPI(title="TP FastAPI Users")
app.include_router(users_router)



@app.get("/")
def hello_fastapi():
    return{"message" : "API FastAPI opérationnelle"}


