#!/usr/bin/env bash
. ./venv/bin/activate
python --version
export FLASK_APP=Life_Scorer
export FLASK_ENV=development
echo $PORT
echo $IP

flask run --host=$IP --port=$PORT #if running on cloud9

#flask run #if running on localhost

