from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .edu_cl_mail import check_login, get_mails_num


class Credentials(BaseModel):
    username: str
    password: str


class LoginCheckResult(BaseModel):
    authenticated: bool


class NumberOfMails(BaseModel):
    numberOfMails: int


app = FastAPI()


@app.post("/api/login_check", response_model=LoginCheckResult)
def login_check(c: Credentials):
    login_check_result = check_login(c.username, c.password)
    if not login_check_result:
        raise HTTPException(status_code=401, detail="invalid credentials")
    return {"authenticated": login_check_result}


@app.post("/api/num_mails/{name}", response_model=NumberOfMails)
def num_mails(c: Credentials, name: str):
    """ returns number of mails in the inbox <name>"""
    try:
        mails_num = get_mails_num(c.username, c.password, name)
    except Exception:
        raise HTTPException(status_code=500, detail="internal error")
    return {"numberOfMails": mails_num}
