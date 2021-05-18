# About the API
[Motivation](#Motivation)
[Used libraries](#Used-libraries)
[Used method of retrieving mails](#Used-method-of-retrieving-mails)
[Inbox names](#Inbox-names)
[Mail ids](#Mail-ids)
[Restrictions](#Restrictions)
[Links](#Links)
## Motivation
You can use this API to create a better mailbox than the one on edukacja.cl or JSOS.
It can be really hard to search for information inside those mailboxes, as they offer no filtering / searching functionalities.
## Used libraries
FastAPI was used as a web framework for this project, as it is fast and fully compatible with OpenAPI.
BeautifulSoup4 was used as a web page parser.

## Used method of retrieving mails
Parallel requests are used to retrieve mail data and mails, which are then parsed into objects and returned by API.
Unfortunately, you have to make one request to read a single mail and a single request to get metadata about 5 mails, so keep in mind that there are some [restrictions](#Restrictions).


## Inbox names
There are four available inbox names:

```python
inboxes = [
    'odbiorcza',
    'nadawcza',
    'robocza',
    'usuniete',
]
```
## Mail ids
Mails are indexed from 0 to ${inbox_mail_num} - 1.
You can retrieve the ${inbox_mail_num} from the `/api/num_mails/${name}` route, where ${name} is the inbox name.
First mail in the inbox will have and id of 0.
## Restrictions
Be careful about how many mails at once you want to retrieve.
You should not try to download more than 200 mails at once, as Edukacja.cl may block some of the requests, and the result will be an internal error (code 500).
It is better to split the request in chunks, for example keep requesting in chunks of 10 mails, but start a new request after the last one.
## Links
API used on my website: https://krzysztofruczkowski.pl/edu-cl-api/

Docs of API used on my website (sending requests will not work there though, as it is behind a reversed proxy): https://krzysztofruczkowski.pl/edu-cl-api/docs

UI that uses this API: https://krzysztofruczkowski.pl/edu-cl-mail/

API github repository: https://github.com/tojatos/edu-cl-mail

UI github repository: https://github.com/tojatos/edu-cl-mail-front/tree/fastapi
