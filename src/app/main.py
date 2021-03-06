from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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
    sender: str
    row_id: str
    title: str
    priority: str
    date: str
    message: str


class NadawczaMail(BaseModel):
    id: int
    row_id: str
    date: str
    title: str
    message: str
    priority: str
    receiver: str
    send_status: str
    dist_status: str


class RoboczaMail(BaseModel):
    id: int
    row_id: str
    date: str
    title: str
    message: str
    priority: str
    receiver: str


class UsunieteMail(BaseModel):
    id: int
    date: str
    row_id: str
    title: str
    message: str
    priority: str
    receiver: str
    sender: str


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://localhost",
    "https://krzysztofruczkowski.pl:2020",
    "https://krzysztofruczkowski.pl",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.post("/api/mail_range/odbiorcza/{from_}/{to_}", response_model=List[OdbiorczaMail])
def mail_range_odbiorcza(c: Credentials, from_: int, to_: int):
    """ returns mails with ids from range {from_} - {to_} in the inbox 'odbiorcza'"""
    try:
        mails = get_mail_range(c.username, c.password, from_, to_, "odbiorcza")
    except Exception:
        raise HTTPException(status_code=500, detail="internal error")
    return mails


@app.post("/api/mail_range/nadawcza/{from_}/{to_}", response_model=List[NadawczaMail])
def mail_range_nadawcza(c: Credentials, from_: int, to_: int):
    """ returns mails with ids from range {from_} - {to_} in the inbox 'nadawcza'"""
    try:
        mails = get_mail_range(c.username, c.password, from_, to_, "nadawcza")
    except Exception:
        raise HTTPException(status_code=500, detail="internal error")
    return mails


@app.post("/api/mail_range/robocza/{from_}/{to_}", response_model=List[RoboczaMail])
def mail_range_robocza(c: Credentials, from_: int, to_: int):
    """ returns mails with ids from range {from_} - {to_} in the inbox 'robocza'"""
    try:
        mails = get_mail_range(c.username, c.password, from_, to_, "robocza")
    except Exception:
        raise HTTPException(status_code=500, detail="internal error")
    return mails


@app.post("/api/mail_range/usuniete/{from_}/{to_}", response_model=List[UsunieteMail])
def mail_range_usuniete(c: Credentials, from_: int, to_: int):
    """ returns mails with ids from range {from_} - {to_} in the inbox 'usuniete'"""
    try:
        mails = get_mail_range(c.username, c.password, from_, to_, "usuniete")
    except Exception:
        raise HTTPException(status_code=500, detail="internal error")
    return mails
