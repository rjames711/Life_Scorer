from flask import Blueprint, redirect, url_for,session, request,jsonify
import Life_Scorer.user as user
import Life_Scorer.interface as interface
from functools import wraps
import datetime
import Life_Scorer.tools as tools
import Life_Scorer.scoring as scoring
import Life_Scorer.sum_by_day as sum_by_day
import Life_Scorer.custom_stats as cus_stats_module
noncors_api = Blueprint('api', __name__)
import json

#I can't figure out how to import from __init__ so copied over.
def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        #Changed below to use session instead of g.
        if 'username' not in session:
            print('no user in login required')
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

def get_user():
    return session['username']

@noncors_api.route("/dayscores_cat")
@login_required
def get_category_scores():
    cat_id= int(request.args.get('cat_id'))
    if cat_id == 0:
        return get_day_scores()
    numdays= int(request.args.get('numdays'))
    offset= int(request.args.get('offset'))
    days = tools.get_days(numdays,offset)
    dayscores=[]
    for day in days:
        dayscores.append(scoring.get_day_score_by_category( day, get_user(), cat_id))
    res = [ dayscores , days ]
    return json.dumps(res)

@noncors_api.route("/dayscores")
@login_required
def get_day_scores():
    numdays= int(request.args.get('numdays'))
    offset= int(request.args.get('offset'))
    days = tools.get_days(numdays,offset)
    dayscores=[]
    for day in days:
        dayscores.append(scoring.get_day_score( day, get_user()))
    res = [ dayscores , days ]
    return json.dumps(res)

@noncors_api.route("/tasks")
@login_required
def tasks():
    tasks = interface.read_tasks(get_user())
    tasks = [task.__dict__ for task in tasks]
    return json.dumps(tasks)
