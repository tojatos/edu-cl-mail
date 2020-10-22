import requests
from bs4 import BeautifulSoup
import re

def get_all_mails(login, password):
    return get_mails(login, password, -1)

def get_mails(login, password, max_mails):
    '''-1 in max_mails means infinity'''
    base_url = 'https://edukacja.pwr.wroc.pl/EdukacjaWeb/studia.do'
    inbox_url = 'https://edukacja.pwr.wroc.pl/EdukacjaWeb/zawartoscSkrzynkiPocztowej.do'
    mail_content_url = 'https://edukacja.pwr.wroc.pl/EdukacjaWeb/podgladWiadomosci.do'

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

    def get_mail_content(row_id):
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
        return content.split('-->')[-1].replace('<br/>','').replace('</td>', '').replace('\r', '\n').strip()

    def get_five_mails(paging_range_start):
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
                temp_data['message'] = get_mail_content(row_id)
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

    max_index = min(last_page_num * 5, max_mails)

    flatten = lambda t: [item for sublist in t for item in sublist]
    mails = flatten([get_five_mails(i) for i in range(0, max_index, 5)])[:max_mails]
    return mails