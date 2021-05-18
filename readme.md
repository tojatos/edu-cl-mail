# Edukacja.cl inbox API

Currently, supports only reading mails.

No login data is stored while using this API.

## Why
Because using the native website is not the most enjoyable experience.

## API specification
After you run this API, navigate to `http://localhost/docs` (or to `${YOUR_HOST}/docs`, if you are using a different host)
You will see available routes and schemas.

## How to run this
### With docker-compose
Modify docker-compose.yml and run it:
```shell
docker-compose up
```
### With docker
Navigate to `src` directory, build and tag the image, and then run it, for example:
```shell
docker build -t edu_cl_fastapi .
docker run -p 80:80 edu_cl_fastapi:latest
```

## Testing
### Environment variables
You will need to set the following environment variables (or just populate `.env` file at the root of the `src` directory):

| Variable | Description |
| --- | --- |
| LOGIN | your edukacja.cl login |
| PASSWORD | your edukacja.cl password |

### Running tests
Go to the `src` directory and run:
```shell
python -m pytest tests --disable-pytest-warnings -n3
```
or, if you use Windows, you can just run the `test.ps1` script.
