from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .edu_cl_mail import check_login


class Credentials(BaseModel):
    username: str
    password: str



class LoginCheckResult(BaseModel):
    authenticated: bool

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/login_check", response_model=LoginCheckResult)
def login_check(c: Credentials):
    """ returns "true", "false" or "invalid credentials or internal error" """
    login_check_result = check_login(c.username, c.password)
    if not login_check_result:
        raise HTTPException(status_code=401, detail="invalid credentials or internal error")
    return {"authenticated": login_check_result}
