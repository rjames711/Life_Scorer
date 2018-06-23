import json
from pprint import pprint
attr = '{ "attr":["reps","lbs"], "mod":0.015, "val_defaults": {"min": 45 , "max":200, "default":135}  }'
log = '{"reps":10, "lbs":135}'

entry = json.loads(log)
attributes = json.loads(attr)

def score_entry(entry, attributes):
  score = 1
  for attr in entry:
    score *= entry[attr]
  return score * attributes['mod']
