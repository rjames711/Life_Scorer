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

bp = Blueprint('catdog', __name__, url_prefix='/catdog')

def token_required(view):
   @wraps(view)
   def wrapped_view(**kwargs):
      token = kwargs['token']
      good_token = user.get_token(kwargs['user'])
      if token != good_token:
         return 'no love'
      return view(**kwargs)
   return wrapped_view


@bp.route('/')
def catdog():
    return render_template('catdog.html', pics = get_catdog_pics())

def get_catdog_pics():
   pics = os.listdir('static/catdogpics')
   pics = [ os.path.join('static/catdogpics',x) for x in pics]
   return pics

