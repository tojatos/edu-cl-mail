import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat

base_url = 'https://edukacja.pwr.wroc.pl/EdukacjaWeb/studia.do'
inbox_url = 'https://edukacja.pwr.wroc.pl/EdukacjaWeb/zawartoscSkrzynkiPocztowej.do'
mail_content_url = 'https://edukacja.pwr.wroc.pl/EdukacjaWeb/podgladWiadomosci.do'
login_url = 'https://edukacja.pwr.wroc.pl/EdukacjaWeb/logInUser.do'

id_skrzynek = {
    'odbiorcza': 1246406,
    'nadawcza': 1246405,
    'robocza': 1246407,
    'usuniete': 1246404,
}

def get_mail_content(row_id, s, web_session_token):
    mail_content_params = {
        'clEduWebSESSIONTOKEN': web_session_token,
        'event': 'positionRow',
        'positionIterator': 'WiadomoscWSkrzynceViewIterator',
        'rowId': row_id,
    }
    mail_content_res = s.get(mail_content_url, params=mail_content_params)

    mail_content_soup = BeautifulSoup(mail_content_res.content, 'html.parser')

    table = mail_content_soup.find('table', {'class': 'KOLOROWA'})
    tds = table.find_all('td', class_='BIALA')
    content = str(tds[15])
    return content.split('-->')[-1].replace('</br>', '').replace('<br>', '').replace('<br/>','\n').replace('</td>', '').replace('\r', '').strip()

def get_messages_datas(tds, headers, s, web_session_token):
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
            row_id = re.findall(r'rowId=(.*)&',td.find('a').attrs['href'])[0]
            temp_data['message'] = get_mail_content(row_id, s, web_session_token)

        i += 1
        if i % len(headers) == 0:
            i = 0
            messages_datas.append(temp_data)
            temp_data = {}

    return messages_datas

def get_five_mails(paging_range_start, s, web_token, web_session_token):
    '''get five mails from paging_range_start'''
    inbox_data = {
        'cl.edu.web.TOKEN': web_token,
        'clEduWebSESSIONTOKEN': web_session_token,
        'pagingIterName': 'WiadomoscWSkrzynceViewIterator',
        'pagingRangeStart': paging_range_start,
        'event': 'positionIterRangeStart',
    }

    inbox_res = s.post(inbox_url, data=inbox_data)
    inbox_soup = BeautifulSoup(inbox_res.content, 'html.parser')

    table = inbox_soup.find('table', {'class': 'KOLOROWA'})

    header_tds = table.find_all('td', class_='NAGLOWEK')
    headers = [x.text.strip() for x in header_tds]
    tds = table.find_all('td', class_='BIALA')

    messages_datas = get_messages_datas(tds, headers, s, web_session_token)

    return messages_datas

def get_mails(login, password, max_mails, inbox='odbiorcza'):
    '''-1 in max_mails means infinity'''

    inbox_id = id_skrzynek[inbox]

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

    inbox_init_params = {
        'clEduWebSESSIONTOKEN': web_session_token,
        'cl.edu.web.TOKEN': web_token,
        'event': 'positionPostBox',
        'rowId': inbox_id,
        'SkrzynkaWiadomosciTable': inbox_id,
        'positionIterator': 'SkrzynkaWiadomosciROViewIterator',
    }

    # init inbox, following post requests will not work otherwise
    inbox_init_res = s.get(inbox_url, params=inbox_init_params)

    paging_numerics = BeautifulSoup(inbox_init_res.content, 'html.parser').find_all('input', class_='paging-numeric-btn')
    if not paging_numerics: # only one page
        last_page_num = 1
    else:
        last_page_num = int(paging_numerics[-1].get('value'))

    if max_mails == -1:
        max_mails = last_page_num * 5 + 5

    max_index = min(last_page_num * 5, max_mails)
    indexes = range(0, max_index, 5)

    flatten = lambda t: [item for sublist in t for item in sublist]

    with ThreadPoolExecutor(max_workers=50) as pool:
        fetched_mails = pool.map(get_five_mails, indexes, repeat(s), repeat(web_token), repeat(web_session_token))

        result_mails = flatten(fetched_mails)[:max_mails]

        return result_mails


def get_amount_inbox(login, password, amount, inbox):
    return get_mails(login, password, amount, inbox)

def get_all_inbox(login, password, inbox):
    return get_mails(login, password, -1, inbox)

def get_all_mails(login, password):
    return get_mails(login, password, -1)
