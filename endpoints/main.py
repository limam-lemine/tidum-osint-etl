from fastapi import FastAPI
from model.domain import Domain

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hey"}

@app.post("/domain/submit")
async def get_domain(domain: Domain):
    return None