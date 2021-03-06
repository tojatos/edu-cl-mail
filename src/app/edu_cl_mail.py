import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from dataclasses import dataclass


@dataclass
class EduClAuth:
    session: requests.sessions.Session
    web_token: str
    web_session_token: str


@dataclass
class EduClAuthFail:
    pass


base_url = 'https://edukacja.pwr.wroc.pl/EdukacjaWeb/studia.do'
inbox_url = 'https://edukacja.pwr.wroc.pl/EdukacjaWeb/zawartoscSkrzynkiPocztowej.do'
mail_content_url = 'https://edukacja.pwr.wroc.pl/EdukacjaWeb/podgladWiadomosci.do'
login_url = 'https://edukacja.pwr.wroc.pl/EdukacjaWeb/logInUser.do'

inbox_ids = {
    'odbiorcza': 0,
    'nadawcza': 1,
    'robocza': 2,
    'usuniete': 3,
}


def get_mail_content(row_id: str, edu_cl_auth: EduClAuth):
    """returns mail content for given row_id"""
    mail_content_params = {
        'clEduWebSESSIONTOKEN': edu_cl_auth.web_session_token,
        'event': 'positionRow',
        'positionIterator': 'WiadomoscWSkrzynceViewIterator',
        'rowId': row_id,
    }
    mail_content_res = edu_cl_auth.session.get(mail_content_url, params=mail_content_params)

    mail_content_soup = BeautifulSoup(mail_content_res.content, 'html.parser')

    content = str(mail_content_soup.find(string=re.compile('Treść:')).parent.find_next('td'))
    content = content.split('-->')[-1].replace('</br>', '').replace('<br>', '').replace('<br/>', '\n')
    return content.replace('</td>', '').replace('\r', '').strip()


def get_messages_data_list(tds, headers):
    """returns messages metadata from unparsed HTML"""

    header_to_json_key_map = {
        '': '',
        '!': '',
        'Od': 'sender',
        'Temat': 'title',
        'Priorytet': 'priority',
        'Do': 'receiver',
        'Status nad.': 'send_status',
        'Status dystr.': 'dist_status',
        'Data otrzymania': 'date',
        'Data wysłania': 'date',
        'Data utworzenia': 'date',
        'Data usunięcia': 'date',
    }

    i = 0

    messages_datas = []
    temp_data = {}
    for td in tds:
        json_key = header_to_json_key_map[headers[i]]
        if not json_key:
            i += 1
            continue
        temp_data[json_key] = td.text.strip()
        if json_key == 'title':
            row_id = re.findall(r'rowId=(.*)&', td.find('a').attrs['href'])[0]
            temp_data['row_id'] = row_id

        i += 1
        if i % len(headers) == 0:
            i = 0
            messages_datas.append(temp_data)
            temp_data = {}

    return messages_datas


def get_five_mails(paging_range_start: int, edu_cl_auth: EduClAuth):
    """get five mails from paging_range_start (or potentially less if this is at the end of paging) """
    inbox_data = {
        'cl.edu.web.TOKEN': edu_cl_auth.web_token,
        'clEduWebSESSIONTOKEN': edu_cl_auth.web_session_token,
        'pagingIterName': 'WiadomoscWSkrzynceViewIterator',
        'pagingRangeStart': paging_range_start,
        'event': 'positionIterRangeStart',
    }

    inbox_res = edu_cl_auth.session.post(inbox_url, data=inbox_data)
    inbox_soup = BeautifulSoup(inbox_res.content, 'html.parser')

    table = inbox_soup.find('table', {'class': 'KOLOROWA'})

    header_tds = table.find_all('td', class_='NAGLOWEK')
    headers = [x.text.strip() for x in header_tds]
    tds = table.find_all('td', class_='BIALA')

    messages_data_list = get_messages_data_list(tds, headers)

    return messages_data_list


def get_inbox_real_id(inbox: str, edu_cl_auth: EduClAuth):
    """ returns real id of inbox """
    inbox_id = inbox_ids[inbox]

    inbox_params = {
        'clEduWebSESSIONTOKEN': edu_cl_auth.web_session_token,
        'cl.edu.web.TOKEN': edu_cl_auth.web_token,
        'event': 'defaultPostBox',
    }

    inbox_res = edu_cl_auth.session.get(inbox_url, params=inbox_params)
    options = BeautifulSoup(inbox_res.content, 'html.parser').find('select', id='wyborSkrzynek').findChildren('option')
    inbox_real_id = options[inbox_id].attrs['value']
    return inbox_real_id


def init_inbox(inbox, edu_cl_auth: EduClAuth):
    """init inbox, following post requests will not work otherwise"""
    inbox_real_id = get_inbox_real_id(inbox, edu_cl_auth)

    inbox_init_params = {
        'clEduWebSESSIONTOKEN': edu_cl_auth.web_session_token,
        'cl.edu.web.TOKEN': edu_cl_auth.web_token,
        'event': 'positionPostBox',
        'rowId': inbox_real_id,
        'SkrzynkaWiadomosciTable': inbox_real_id,
        'positionIterator': 'SkrzynkaWiadomosciROViewIterator',
    }

    inbox_init_res = edu_cl_auth.session.get(inbox_url, params=inbox_init_params)
    return inbox_init_res


def get_last_page_num(inbox_init_res):
    """returns last page number from initialized inbox"""
    paging_numerics = BeautifulSoup(inbox_init_res.content, 'html.parser').find_all('input',
                                                                                    class_='paging-numeric-btn')
    if not paging_numerics:  # only one page
        return 1
    return int(paging_numerics[-1].get('value'))


def get_edu_cl_auth(login: str, password: str):
    """returns EduClAuth object if user can login, otherwise returns EduClAuthFail"""
    s = requests.Session()

    req = s.get(base_url)
    soup = BeautifulSoup(req.content, 'html.parser')
    web_token = soup.find('input', {'name': 'cl.edu.web.TOKEN'}).get('value')

    data = {
        'cl.edu.web.TOKEN': web_token,
        'login': login,
        'password': password,
    }

    login_res = s.post(login_url, data=data)
    login_soup = BeautifulSoup(login_res.content, 'html.parser')

    web_session_token = login_soup.find('input', {'name': 'clEduWebSESSIONTOKEN'}).get('value')
    logged_in_element = login_soup.find('td', class_='ZALOGOWANY_UZYT')
    login_successful = logged_in_element is not None
    if login_successful:
        return EduClAuth(s, web_token, web_session_token)
    return EduClAuthFail()


def check_login(login: str, password: str):
    """returns true if credentials can be used to login, false otherwise"""
    edu_cl_auth = get_edu_cl_auth(login, password)
    return type(edu_cl_auth) is not EduClAuthFail


def get_mails_num_auth(edu_cl_auth: EduClAuth, last_page_num: int) -> int:
    """returns number of mails from initialized inbox"""
    return len(get_five_mails(last_page_num * 5 - 5, edu_cl_auth)) + (last_page_num - 1) * 5


def get_mails_num(login: str, password: str, inbox: str) -> int:
    """returns number of mails from inbox"""
    edu_cl_auth = get_edu_cl_auth(login, password)
    inbox_init_res = init_inbox(inbox, edu_cl_auth)
    return get_mails_num_auth(edu_cl_auth, get_last_page_num(inbox_init_res))


def get_mail_range(login: str, password: str, from_: int, to_: int, inbox: str = "odbiorcza"):
    """returns mails from range <from_> - <to_> in inbox <inbox>"""
    edu_cl_auth = get_edu_cl_auth(login, password)

    inbox_init_res = init_inbox(inbox, edu_cl_auth)
    last_page_num = get_last_page_num(inbox_init_res)
    mails_num = get_mails_num_auth(edu_cl_auth, last_page_num)

    from_ = max(from_, 0)
    to_ = min(to_, mails_num - 1)

    if from_ > to_:
        return []

    number_of_mails_to_fetch = to_ - from_ + 1
    if number_of_mails_to_fetch <= 0:
        return []

    number_of_additional_pages_to_fetch = (number_of_mails_to_fetch - 1) // 5

    paging_range_start = mails_num - to_ - 1
    paging_range_end = paging_range_start + number_of_additional_pages_to_fetch * 5
    all_paging_range_starts = range(paging_range_start, paging_range_end + 1, 5)

    def flatten(t):
        return [item for sublist in t for item in sublist]

    with ThreadPoolExecutor(max_workers=50) as pool:
        fetched_mails = pool.map(get_five_mails, all_paging_range_starts, repeat(edu_cl_auth))

        result_mails = list(reversed(flatten(fetched_mails)[:number_of_mails_to_fetch]))

        fetched_messages = pool.map(get_mail_content, [x["row_id"] for x in result_mails], repeat(edu_cl_auth))

        for index, (mail, message) in enumerate(zip(result_mails, fetched_messages)):
            mail["id"] = from_ + index
            mail["message"] = message

        return result_mails
