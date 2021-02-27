#!/usr/bin/env bash

source ./venv/bin/activate
export FLASK_DEBUG=0
export FLASK_APP=wsgi
export FLASK_ENV=development
flask run 
