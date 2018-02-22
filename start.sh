#!/bin/bash

explorer http://localhost:8010

set -a
source ./.env
set +a

export FLASK_DEBUG=1
export FLASK_APP=app.py
flask run --port=8010
