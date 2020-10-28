#!/usr/bin/env python
import os
import pprint
from app.edu_cl_mail import get_all_mails, get_mails
import time


from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()

    print(f'Logging in {os.environ["LOGIN"]}')

    # all_mails = get_all_mails(os.environ['LOGIN'], os.environ['PASSWORD'])

    start = time.time()
    # mails = get_mails(os.environ['LOGIN'], os.environ['PASSWORD'], 50)
    mails = get_all_mails(os.environ['LOGIN'], os.environ['PASSWORD'])
    end = time.time()
    print("Finished fetching mails, time:")
    print(end - start)
    # pprint.pprint(mails)
    # print(mails[2]['message'])
    print(len(mails))
