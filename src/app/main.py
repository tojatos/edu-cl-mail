from fastapi import FastAPI
from pydantic import BaseModel

from .edu_cl_mail import check_login


class Credentials(BaseModel):
    username: str
    password: str


# class LoginCheckResult(BaseModel):
#     authenticated: bool

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/login_check")
def login_check(c: Credentials):
    """ returns "true", "false" or "invalid credentials or internal error" """
    return check_login(c.username, c.password)
