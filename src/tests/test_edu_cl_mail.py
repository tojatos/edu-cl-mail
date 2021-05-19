import os

from dotenv import load_dotenv

from app.edu_cl_mail import get_edu_cl_auth, EduClAuth, get_mails_num, get_mail_range

load_dotenv()


def get_env(key, fallback):
    try:
        return os.environ[key]
    except KeyError:
        return fallback


USERNAME = get_env('LOGIN', '')
PASSWORD = get_env('PASSWORD', '')


def test_get_edu_cl_auth():
    result = get_edu_cl_auth(USERNAME, PASSWORD)
    assert type(result) is EduClAuth


def test_get_mail_num():
    """assumes you have at least 1 mail in this inbox"""
    result = get_mails_num(USERNAME, PASSWORD, "odbiorcza")
    assert result > 1


def test_get_mail_range_odbiorcza():
    """assumes you have at least 13 mails in this inbox"""
    from_ = 1
    to_ = 12
    result = get_mail_range(USERNAME, PASSWORD, from_, to_, "odbiorcza")
    assert len(result) == to_ - from_ + 1


def test_get_mail_range_nadawcza():
    """assumes you have at least 3 mails in this inbox"""
    from_ = 0
    to_ = 2
    result = get_mail_range(USERNAME, PASSWORD, from_, to_, "nadawcza")
    assert len(result) == to_ - from_ + 1


def test_get_mail_range_robocza():
    """assumes you have at least 3 mails in this inbox"""
    from_ = 0
    to_ = 2
    result = get_mail_range(USERNAME, PASSWORD, from_, to_, "robocza")
    assert len(result) == to_ - from_ + 1


def test_get_mail_range_usuniete():
    """assumes you have at least 1 mail in this inbox"""
    from_ = 0
    to_ = 0
    result = get_mail_range(USERNAME, PASSWORD, from_, to_, "usuniete")
    assert len(result) == to_ - from_ + 1


def test_get_mail_range_usuniete_too_much():
    """should return as many mails as you have (up to 15)"""
    from_ = 0
    to_ = 15
    num_mails = get_mails_num(USERNAME, PASSWORD, "usuniete")
    result = get_mail_range(USERNAME, PASSWORD, from_, to_, "usuniete")
    assert len(result) == num_mails


def test_get_mail_range_odbiorcza_negative():
    from_ = 0
    to_ = -15
    result = get_mail_range(USERNAME, PASSWORD, from_, to_, "odbiorcza")
    assert len(result) == 0


def test_get_mail_range_usuniete_weird_range():
    """assumes you don't have 500 mails in this inbox"""
    from_ = 500
    to_ = 503
    result = get_mail_range(USERNAME, PASSWORD, from_, to_, "usuniete")
    assert len(result) == 0


def test_get_mail_range_odbiorcza_negative_positive_range():
    """assumes you have at least 5 mails in this inbox"""
    from_ = -5
    to_ = 4
    result = get_mail_range(USERNAME, PASSWORD, from_, to_, "odbiorcza")
    assert len(result) == 5


def test_get_mail_range_odbiorcza_no_duplicates():
    from_ = 470
    to_ = 479
    result = get_mail_range(USERNAME, PASSWORD, from_, to_, "odbiorcza")
    id_map = list(map(lambda m: m["row_id"], result))
    print(result)
    assert len(id_map) == len(set(id_map))
