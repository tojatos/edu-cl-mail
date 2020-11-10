import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat

base_url = 'https://edukacja.pwr.wroc.pl/EdukacjaWeb/studia.do'
inbox_url = 'https://edukacja.pwr.wroc.pl/EdukacjaWeb/zawartoscSkrzynkiPocztowej.do'
mail_content_url = 'https://edukacja.pwr.wroc.pl/EdukacjaWeb/podgladWiadomosci.do'


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
    tds = table.find_all('td', class_='BIALA')

    i = 0

    messages_datas = []
    temp_data = {}
    for td in tds:
        if i == 1:
            temp_data['sender'] = td.text.strip()
        if i == 2:
            temp_data['title'] = td.text.strip()
            row_id = re.findall(r'rowId=(.*)&',td.find('a').attrs['href'])[0]
            temp_data['message'] = get_mail_content(row_id, s, web_session_token)
        if i == 3:
            temp_data['priority'] = td.text.strip()
        if i == 4:
            temp_data['date'] = td.text.strip()

        i += 1
        if i % 5 == 0:
            i = 0
            messages_datas.append(temp_data)
            temp_data = {}

    return messages_datas

def get_mails(login, password, max_mails):
    '''-1 in max_mails means infinity'''

    s = requests.Session()

    req = s.get(base_url)
    soup = BeautifulSoup(req.content, 'html.parser')
    web_token = soup.find('input', {'name': 'cl.edu.web.TOKEN'}).get('value')

    data = {
        'cl.edu.web.TOKEN': web_token,
        'login': login,
        'password': password,
    }

    login_res = s.post('https://edukacja.pwr.wroc.pl/EdukacjaWeb/logInUser.do', data=data)
    login_soup = BeautifulSoup(login_res.content, 'html.parser')

    web_session_token = login_soup.find('input', {'name': 'clEduWebSESSIONTOKEN'}).get('value')

    inbox_init_params = {
        'clEduWebSESSIONTOKEN': web_session_token,
        'event': 'defaultPostBox',
    }

    # init inbox, following post requests will not work otherwise
    inbox_init_res = s.get(inbox_url, params=inbox_init_params)
    last_page_num = int(BeautifulSoup(inbox_init_res.content, 'html.parser').find_all('input', class_='paging-numeric-btn')[-1].get('value'))

    if max_mails == -1:
        max_mails = last_page_num * 5 + 5

    max_index = min(last_page_num * 5, max_mails)
    indexes = range(0, max_index, 5)

    flatten = lambda t: [item for sublist in t for item in sublist]

    with ThreadPoolExecutor(max_workers=50) as pool:
        fetched_mails = pool.map(get_five_mails, indexes, repeat(s), repeat(web_token), repeat(web_session_token))

        result_mails = flatten(fetched_mails)[:max_mails]

        return result_mails

def get_all_mails(login, password):
    return get_mails(login, password, -1)
