#!/bin/bash -e
cd "$(dirname "$0")"

unset DEBUG
python -m app.start_app
