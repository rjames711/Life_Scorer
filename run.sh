#!/usr/bin/env bash
. ./venv/bin/activate
python --version
export FLASK_APP=Life_Scorer
export FLASK_ENV=development
echo $PORT
echo $IP
echo $1

if [ "$1" = "server" ]
then
    echo running on server
    flask run --host=0.0.0.0 --port=5000

elif [ -z "$PORT" ]
then
    echo running on localhost
    flask run #if running on localhost

else
    echo running on cloud9 ide
    flask run --host=$IP --port=$PORT #if running on cloud9
fi

