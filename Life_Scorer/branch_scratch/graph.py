import sys
sys.path.append('..')
import interface as i

data = i.get_log('Rob')

#TODO fix timezone hardcoding below
dt = datetime.datetime.utcnow() -datetime.timedelta(hours=5)
scores = []
for days in range(30):
    offdt = dt - datetime.timedelta(days = days)
    date = str(offdt.date())
    score = get_day_score(date, user)
    scores.append((date, score))
return scores

