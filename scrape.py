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

s = requests.Session()

req = s.get(base_url)
soup = BeautifulSoup(req.content, 'html.parser')
token = soup.find('input', {'name': 'cl.edu.web.TOKEN'}).get('value')

data = {
  'cl.edu.web.TOKEN': token,
  'login': os.environ['LOGIN'],
  'password': os.environ['PASSWORD'],
}

r = s.post('https://edukacja.pwr.wroc.pl/EdukacjaWeb/logInUser.do', data=data)
# print(r.headers)