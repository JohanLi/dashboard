#!/bin/bash

set -a
source ./.env
set +a

export FLASK_DEBUG=1
export FLASK_APP=app.py
flask run
