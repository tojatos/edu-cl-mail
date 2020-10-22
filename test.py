import os
import pprint
from app.edu_cl_mail import get_all_mails

from dotenv import load_dotenv
load_dotenv()

print(f'Logging in {os.environ["LOGIN"]}')

pprint.pprint(get_all_mails(os.environ['LOGIN'], os.environ['PASSWORD']))