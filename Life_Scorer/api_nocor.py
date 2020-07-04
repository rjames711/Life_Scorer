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

@noncors_api.route("/test")
@login_required
def get_category_scores():
    cat_id= int(request.args.get('cat_id'))
    numdays= int(request.args.get('numdays'))
    offset= int(request.args.get('offset'))
    print(cat_id, numdays, offset)
    days = tools.get_days(numdays,offset)
    dayscores=[]
    for day in days:
        dayscores.append(scoring.get_day_score_by_category( day, get_user(), cat_id))
    print(days)
    print(dayscores)
    res = [ dayscores , days ]
    return json.dumps(res)