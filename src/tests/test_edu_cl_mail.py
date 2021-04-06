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


# def test_get_pages_num():
#     result = get_pages_num(USERNAME, PASSWORD, "odbiorcza")
#     assert result > 1


def test_get_mail_num():
    result = get_mails_num(USERNAME, PASSWORD, "odbiorcza")
    assert result > 1


def test_get_mail_range():
    from_ = 1
    to_ = 12
    result = get_mail_range(USERNAME, PASSWORD, from_, to_, "odbiorcza")
    assert len(result) == to_ - from_ + 1

# def test_get_page_to_range_map():
#     assert False
    # result = get_mails_num(USERNAME, PASSWORD, "odbiorcza")
    # assert result > 1


# def test_get_message_row_ids_from_page():
#     assert False
    # result = get_mails_num(USERNAME, PASSWORD, "odbiorcza")
    # assert result > 1
