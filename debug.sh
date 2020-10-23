#!/bin/bash -e
cd "$(dirname "$0")"

export DEBUG=true
export FLASK_ENV=development
python -m app.start_app
