# Parser Edukacja.cl
[1. Opis](#1-opis)

[2. Zródła](#2-%C5%B9r%C3%B3d%C5%82a)

[3. Przykładowe dane](#3-przyk%C5%82adowe-dane)

[4. Opis wywołania](#4-opis-wywo%C5%82ania)

[5. Opis wersji](#5-opis-wersji)

[6. Uruchomienie kontenera z usługą](#6-uruchomienie-kontenera-z-us%C5%82ug%C4%85)

[7. Linki](#7-linki)

## 1. Opis
Skrzynka z elektronicznymi wiadomościami na portalach https://edukacja.pwr.wroc.pl oraz https://jsos.pwr.edu.pl nie pozwala na filtrowanie / szukanie wiadomości.

Można wykorzystać ten parser w celu stworzenia lepszej skrzynki.

## 2. Zródła
[FastAPI](https://fastapi.tiangolo.com/) został użyty jako web framework dla tego projektu, ponieważ jest szybki i w pełni kompatybilny z OpenAPI.

[BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) został użyty jako parser stron internetowych.

## 3. Przykładowe dane
Do skorzystania z API potrzebny jest login i hasło do Edukacja.cl:

```json
{
  "username": "string",
  "password": "string"
}
```

```
username - login do Edukacja.cl
password - hasło do Edukacja.cl
```

## 4. Opis wywołania
Po uruchomieniu tego API, można przejść do http://localhost/docs (lub do ${HOST}/docs, w przypadku użycia innego hosta).

Znajdzie się tam specyfikacja API w standardzie OpenAPI.

### Dostępne skrzynki
```python
inboxes = [
    'odbiorcza',
    'nadawcza',
    'robocza',
    'usuniete',
]
```

### Indeksowanie maili
Maile są indeksowane od 0.
Pierwszy mail w danej skrzynce będzie miał id 0.

### Krótki opis API
```
/api/login_check - pozwala na sprawdzenie loginu i hasła
/api/num_mails/{name} - zwraca liczbę maili dla skrzynki {name}
/api/mail_range/{name}/{from_}/{to_} - zwraca maile dla skrzynki {name} od indeksu {from_} do indeksu {to_}
```

### Ograniczenia
Trzeba uważać na liczbę wiadomości do pobrania za jednym razem.
Nie należy próbować pobierać więcej niż 200 maili naraz, ponieważ system Edukacja.cl może zablokować część żądań, czego wynikiem będzie błąd wewnętrzny (kod 500).
Lepiej jest podzielić żądanie na części, na przykład pobierając w częściach po 10 maili, każde następne żądanie rozpoczynając po ostatnim.

## 5. Opis wersji
Nie dotyczy.

## 6. Uruchomienie kontenera z usługą
### Używając docker-compose'a
Wystarczy zmodyfikować i uruchomić docker-compose.yml:
```shell
docker-compose up
```
### Używając dockera
Po przejściu do folderu `src`, należy zbudować i otagować obraz, a następnie go uruchomić, na pszykład:
```shell
docker build -t edu_cl_fastapi .
docker run -p 80:80 edu_cl_fastapi:latest
```

## 7. Linki

Repozytorium API na githubie: https://github.com/tojatos/edu-cl-mail

Wystawione API: https://krzysztofruczkowski.pl/edu-cl-api/

Specyfikacja wystawionego API (wysyłanie żądań z tej specyfikacji nie zadziała, gdyż jest wystawiona za odwróconym proxy): https://krzysztofruczkowski.pl/edu-cl-api/docs

Przykładowe UI wykorzystujące API: https://krzysztofruczkowski.pl/edu-cl-mail/

Repozytorium UI na githubie: https://github.com/tojatos/edu-cl-mail-front/tree/fastapi
