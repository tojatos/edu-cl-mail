import os
import pprint
from app.edu_cl_mail import get_all_mails, get_mails

from dotenv import load_dotenv
load_dotenv()

print(f'Logging in {os.environ["LOGIN"]}')

# all_mails = get_all_mails(os.environ['LOGIN'], os.environ['PASSWORD'])
# pprint.pprint(all_mails)
# print(len(all_mails))

mails = get_mails(os.environ['LOGIN'], os.environ['PASSWORD'], 21)
pprint.pprint(mails)
print(len(mails))