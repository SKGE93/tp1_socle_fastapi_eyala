from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello_fastapi():
    return{"message" : "API FastAPI opérationnelle"}