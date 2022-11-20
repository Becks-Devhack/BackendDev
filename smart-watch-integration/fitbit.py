import urllib
import requests
import json
from flask import Flask

app = Flask(__name__)

# obtained separately using private infos
access_token='eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzkzN0MiLCJzdWIiOiI5UUxYTU4iLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyYWN0IHJveHkgcnJlcyByaHIgcm51dCBydGVtIHJzbGUiLCJleHAiOjE2Njk0NjcxNjMsImlhdCI6MTY2ODg2Mzk3Nn0.7OtUgSmIddTTzpHhZJBerIg9bcHiKamXXIon_SjfVWA'
header = {'Authorization' : 'Bearer {}'.format(access_token)}

#you can also give date in the url
@app.route("/stress_levels/<string:start_date>/<string:end_date>", methods=["GET"])
def get_data_by_date(start_date, end_date):
	global access_token
	global header
	
	base_url = 'https://api.fitbit.com/1.2/user/-/sleep/date/{}/{}.json'.format(start_date, end_date)
	r = requests.get(base_url, headers=header).json()
	sleep_duration = []
	for i in range(len(r['sleep'])):
		sleep_duration.append(r['sleep'][i].get('duration', 0) / 3600000)

	base_url='https://api.fitbit.com/1/user/-/activities/heart/date/{}/{}/1min.json'.format(start_date, end_date)
	r = requests.get(base_url, headers=header).json()
	resting_heart_rate = []
	for i in range(len(r['activities-heart'])):
		resting_heart_rate.append(r['activities-heart'][i]['value'].get('restingHeartRate', 0))


	base_url='https://api.fitbit.com/1/user/-/br/date/{}/{}.json'.format(start_date, end_date)
	r = requests.get(base_url, headers=header).json()
	breathing_rate = []
	for i in range(len(r['br'])):
		breathing_rate.append(r['br'][i]['value'].get('breathingRate', 0))

	return json.dumps({
		"breathing_rate": breathing_rate,
		"sleep_hrs": sleep_duration,
		"heart_rate": resting_heart_rate
		})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)