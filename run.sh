. /home/ubuntu/workspace/Life_Scorer/venv/bin/activate
python --version
export FLASK_APP=app.py
export FLASK_ENV=development
echo $PORT
echo $IP
flask run --host=$IP --port=$PORT
