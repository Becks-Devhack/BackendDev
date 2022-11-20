import urllib
import requests
import json
from flask import Flask

app = Flask(__name__)

# obtained separately using private infos
access_token='eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzkzN0MiLCJzdWIiOiI5UUxYTU4iLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyYWN0IHJveHkgcnJlcyByaHIgcm51dCBydGVtIHJzbGUiLCJleHAiOjE2Njk0NjcxNjMsImlhdCI6MTY2ODg2Mzk3Nn0.7OtUgSmIddTTzpHhZJBerIg9bcHiKamXXIon_SjfVWA'
header = {'Authorization' : 'Bearer {}'.format(access_token)}

#default returns today's data
@app.route("/stress_levels", methods=["GET"])
def get_today_data():
	global access_token
	global header

	base_url = 'https://api.fitbit.com/1/user/-/sleep/date/today.json'
	r = requests.get(base_url, headers=header).json()
	if 'summary' in r:
		sleep_duration = r['summary']['totalMinutesAsleep']
	else:
		sleep_duration = 0

	base_url='https://api.fitbit.com/1/user/-/activities/heart/date/today/today/1min.json'
	r = requests.get(base_url, headers=header).json()
	if 'activities-heart' in r:
		if 'restingHeartRate' in r['activities-heart'][0]['value']:
			resting_heart_rate = r['activities-heart'][0]['value']['restingHeartRate']
		else:
			resting_heart_rate = 0

	else:
		resting_heart_rate = 0

	base_url='  https://api.fitbit.com/1/user/-/br/date/today.json'
	r = requests.get(base_url, headers=header).json()
	if 'br' in r:
		if len(r['br']):
			breathing_rate = r['br'][0]['value']['breathingRate']
		else:
			breathing_rate = 0
	else:
		breathing_rate = 0

	return json.dumps({
		"breathing_rate": breathing_rate,
	    "sleep_hrs": sleep_duration / 3600000,
	    "heart_rate": resting_heart_rate
	})

#you can also give date in the url
@app.route("/stress_levels/<string:date>", methods=["GET"])
def get_data_by_date(date):
	global access_token
	global header
	
	base_url = 'https://api.fitbit.com/1/user/-/sleep/date/{}.json'.format(date)
	r = requests.get(base_url, headers=header).json()
	if 'summary' in r:
		sleep_duration = r['summary']['totalMinutesAsleep']
	else:
		sleep_duration = 0

	base_url='https://api.fitbit.com/1/user/-/activities/heart/date/{}/{}/1min.json'.format(date, date)
	r = requests.get(base_url, headers=header).json()
	if 'activities-heart' in r:
		if 'restingHeartRate' in r['activities-heart'][0]['value']:
			resting_heart_rate = r['activities-heart'][0]['value']['restingHeartRate']
		else:
			resting_heart_rate = 0

	else:
		resting_heart_rate = 0

	base_url='  https://api.fitbit.com/1/user/-/br/date/{}.json'.format(date)
	r = requests.get(base_url, headers=header).json()
	if 'br' in r:
		if len(r['br']):
			breathing_rate = r['br'][0]['value']['breathingRate']
		else:
			breathing_rate = 0
	else:
		breathing_rate = 0

	return r
	#json.dumps({
	#	"breathing_rate": breathing_rate,
	#	"sleep_hrs": sleep_duration / 60,
	#	"heart_rate": resting_heart_rate
	#	})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)