#!/usr/bin/env bash

source ./venv/bin/activate
export FLASK_DEBUG=1
export FLASK_APP=wsgi
flask run 