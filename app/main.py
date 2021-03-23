from fastapi import FastAPI
from pydantic import BaseModel

class Credentials(BaseModel):
    username: str
    password: str

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
