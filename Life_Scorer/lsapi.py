from flask import (
   Flask, Blueprint, flash, g, redirect, render_template, request, url_for, session
)
import os 
print (os.getcwd())
import Life_Scorer.user as user
import Life_Scorer.interface as interface
from functools import wraps
import datetime
import Life_Scorer.tools as tools
import Life_Scorer.scoring as scoring
import Life_Scorer.user as user
import Life_Scorer.sum_by_day as sum_by_day
import json
from flask_cors import CORS

#from flaskr.db import get_db

bp = Blueprint('lsapi', __name__, url_prefix='/lsapi')

def token_required(view):
   @wraps(view)
   def wrapped_view(**kwargs):
      token = kwargs['token']
      good_token = user.get_token(kwargs['user'])
      if token != good_token:
         return 'no love'
      return view(**kwargs)
   return wrapped_view


@bp.route('/<user>/tasks/<token>')
@token_required
def tasks(user, token):
   tasks = interface.read_tasks(user)
   tasks = [task.__dict__ for task in tasks]
   return json.dumps(tasks)


@bp.route('/<user>/dayscore/<date>/<token>')
@token_required
def dayscore(user, date,token):
   score = {'score': scoring.get_day_score(date,'Rob') }
   return json.dumps(score)

@bp.route('/<user>/log/<token>')
@token_required
def log(user,token):
   log = interface.get_log(user)
   #Need to get it formatted correctly for json, Feel like this is a slow and bad way to do it but it works
   log = [list(item) for item in log] 
   for item in log:
      item[2] = json.loads(item[2])
   return json.dumps(log)
