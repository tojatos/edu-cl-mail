# Edukacja.cl inbox API

Currently, supports only reading mails.

No login data is stored while using this API.

## Why
Because using the native website is not the most enjoyable experience.

## API specification
For now, you can look at `app/start_app.py` to see available routes

## How to run this
Requirements: python 3.7 or higher
### Environment variables
You can use the following environment variables to tweak the application (just populate `.env` file at the root of this repository):

| Variable | Description | Default |
| --- | --- | --- |
| HOST | the hostname to listen on | '0.0.0.0' |
| PORT | port used in production | 80 |
| DEBUG_PORT | port used in development | 8099 |
| SSL_CERT_LOCATION | location of the ssl cert | 'cert.pem' |
| SSL_CERT_KEY_LOCATION | location of the ssl cert key | 'key.pem' |

### Powershell
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
.\debug.ps1 # or .\run.ps1 for production
```
### Bash / zsh
```shell
./setupenv.sh
source .venv/bin/activate
./debug.sh # or ./run.sh for production
```

## Systemd service
In production, you may want to use the systemd service located at `system_files/edu-cl-api.service`.
Just adjust the `ExecStart` and  `WorkingDirectory` variables to correct values on your system and execute as root:
```shell
systemctl link $(realpath system_files/edu-cl-api.service)
systemctl enable --now edu-cl-api
```
