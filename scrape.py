import requests
import pprint
import os
from bs4 import BeautifulSoup

from dotenv import load_dotenv
load_dotenv()

print(f'Logging in {os.environ["LOGIN"]}')

# to fix printing on Windows
import sys
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

base_url = 'https://edukacja.pwr.wroc.pl/EdukacjaWeb/studia.do'
login_url = 'https://edukacja.pwr.wroc.pl/EdukacjaWeb/logInUser.do'
inbox_url = 'https://edukacja.pwr.wroc.pl/EdukacjaWeb/zawartoscSkrzynkiPocztowej.do'

s = requests.Session()

req = s.get(base_url)
soup = BeautifulSoup(req.content, 'html.parser')
web_token = soup.find('input', {'name': 'cl.edu.web.TOKEN'}).get('value')

print(web_token)

data = {
    'cl.edu.web.TOKEN': web_token,
    'login': os.environ['LOGIN'],
    'password': os.environ['PASSWORD'],
}

login_res = s.post('https://edukacja.pwr.wroc.pl/EdukacjaWeb/logInUser.do', data=data)
login_soup = BeautifulSoup(login_res.content, 'html.parser')

web_session_token = login_soup.find('input', {'name': 'clEduWebSESSIONTOKEN'}).get('value')
print(web_session_token)

inbox_init_params = {
    'clEduWebSESSIONTOKEN': web_session_token,
    'event': 'defaultPostBox',
}

# init inbox, following post requests will not work otherwise
s.get(inbox_url, params=inbox_init_params)

def write_soup(soup):
    import codecs
    with codecs.open('text.html', 'w', encoding='utf8') as f:
        f.write(str(soup))


def get_messages_datas(paging_range_start):
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
            temp_data['link'] = td.find('a').attrs['href']
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

pprint.pprint(get_messages_datas('0'))
pprint.pprint(get_messages_datas('5'))