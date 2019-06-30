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
import Life_Scorer.sum_by_day as sum_by_day
import json
from flask_cors import CORS

#from flaskr.db import get_db

bp = Blueprint('lsapi', __name__, url_prefix='/lsapi')

@bp.route('/<user>/<token>')
def lsapi(user, token):
   good_token = open('token.txt','r').read()
   good_token = good_token.strip('\n')
   if token != good_token:
         return 'no love'
   tasks = interface.read_tasks(user)
   tasks = [task.__dict__ for task in tasks]
   return json.dumps(tasks)
