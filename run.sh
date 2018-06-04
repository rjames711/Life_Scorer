#!/usr/bin/env bash
. ./venv/bin/activate
python --version
export FLASK_APP=Life_Scorer
export FLASK_ENV=development
echo $PORT
echo $IP
if [-z $PORT]
then
    flask run --host=$IP --port=$PORT
else
    flask run
fi
