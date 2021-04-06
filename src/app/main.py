import datetime
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .edu_cl_mail import check_login, get_mails_num, get_mail_range


class Credentials(BaseModel):
    username: str
    password: str


class LoginCheckResult(BaseModel):
    authenticated: bool


class NumberOfMails(BaseModel):
    numberOfMails: int


class OdbiorczaMail(BaseModel):
    id: int
    date: str
    title: str
    message: str
    priority: str
    sender: str


class NadawczaMail(BaseModel):
    id: int
    date: str
    title: str
    message: str
    priority: str
    receiver: str
    send_status: str
    dist_status: str


class RoboczaMail(BaseModel):
    id: int
    date: str
    title: str
    message: str
    priority: str
    receiver: str
    send_status: str
    dist_status: str


class UsunieteMail(BaseModel):
    id: int
    date: str
    title: str
    message: str
    priority: str
    receiver: str
    sender: str


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


# @app.post("/api/mail_range/odbiorcza/{from_}/{to_}", response_model=List[OdbiorczaMail])
@app.post("/api/mail_range/odbiorcza/{from_}/{to_}")
def num_mails(c: Credentials, from_: int, to_: int):
    """ returns mails with ids from range {from_} - {to_} in the inbox 'odbiorcza'"""
    try:
        mails = get_mail_range(c.username, c.password, from_, to_, "odbiorcza")
    except Exception:
        raise HTTPException(status_code=500, detail="internal error")
    return mails
