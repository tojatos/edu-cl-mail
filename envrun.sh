#!/bin/bash -e
cd "$(dirname "$0")"

./setupenv.sh
source .venv/bin/activate
./run.sh
