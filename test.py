#!/usr/bin/env python
import os
import pprint
from app.edu_cl_mail import get_all_mails, get_mails, get_mails_num, get_pages_num
import time


from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()

    print(f'Logging in {os.environ["LOGIN"]}')

    # all_mails = get_all_mails(os.environ['LOGIN'], os.environ['PASSWORD'])

    start = time.time()
    # mails = get_mails(os.environ['LOGIN'], os.environ['PASSWORD'], 20)
    mails = get_mails(os.environ['LOGIN'], os.environ['PASSWORD'], 5, 'nadawcza')
    # mails = get_mails(os.environ['LOGIN'], os.environ['PASSWORD'], 5, 'odbiorcza')
    # mails = get_all_mails(os.environ['LOGIN'], os.environ['PASSWORD'])
    end = time.time()
    print("Finished fetching mails, time:")
    print(end - start)
    # pprint.pprint(mails)
    # print(mails[2]['message'])
    print(len(mails))
    print(mails[1])
    print(get_mails_num(os.environ['LOGIN'], os.environ['PASSWORD'], 'odbiorcza'))
    print(get_pages_num(os.environ['LOGIN'], os.environ['PASSWORD'], 'odbiorcza'))
    print(get_mails_num(os.environ['LOGIN'], os.environ['PASSWORD'], 'nadawcza'))
    print(get_pages_num(os.environ['LOGIN'], os.environ['PASSWORD'], 'nadawcza'))
