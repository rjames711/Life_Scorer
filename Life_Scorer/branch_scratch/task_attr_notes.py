import json
from pprint import pprint
attributes = """{"attr":
            {"reps":
              {"min": 0 , "max":30, "default":10, "score":1}, 
              "lbs":
              {"min": 45 , "max":200, "default":135, "score":1}
            },
            "default_score":20}
            """
log = '{"reps":10, "lbs":135}'



entry = json.loads(log)
attributes = json.loads(attributes)

#Tested and seems to be working

def score_entry(entry, attributes):
  score = 1
  default_qty = 1
  for attr in entry:
    if attributes['attr'][attr]['score']:
      score *= entry[attr]
      default_qty *= attributes['attr'][attr]["default"]
  mod = attributes['default_score']/(default_qty)
  return score * mod
