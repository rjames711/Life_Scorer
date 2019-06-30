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

@bp.route('/<token>')
def lsapi(token):
    if token != 'aa5bbc26-9375-4952-9546-0a30cf5feeb8':
        return "no love"
    #tasks = interface.read_tasks(get_user())
    tasks = interface.read_tasks('Rob')
    tasks = [task.__dict__ for task in tasks]
    return json.dumps(tasks)
