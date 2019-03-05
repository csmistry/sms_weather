#Project: SMS WEATHER
#Date: 02/21/19
#Author: Chintan Mistry
#Description: This API responds to the incoming sms with the appropriate weather data.

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

degree = u'\N{DEGREE SIGN}'

def get_weather(api, city_id):

	#input city is formatted into {} 
	url = "http://api.openweathermap.org/data/2.5/weather?q=" + city_id + "&appid=" + api + "&units=metric"

	#HTTP request to get the data from OpenWeather API, sending the url as a parameter
	res = requests.get(url)

	#This gives us data in json format
	data = res.json()

	#Accessing specific details
	weather_data = "=============" + "\n"*2 + "Current Temp: " + str(data['main']['temp']) + degree + "C" + "\n"*2 + "Max Temp: " + str(data['main']['temp_max']) + degree + "C" + "\n"*2 + "Min Temp: " + str(data['main']['temp_min']) + degree + "C" + "\n"*2 + "Wind Speed: " + str(data['wind']['speed']) + " m/s" + "\n"*2 + "Currently:" + str(data['weather'][0]['description'])
	return weather_data
	
	
#This shows how the server can reply to a request
weather_api = "<OpenWeather API key>"

app = Flask(__name__)

	
@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
	if request.method == 'POST':
		city = request.form['Body']
		data1 = get_weather(weather_api, city)
		
		#Start response
		resp = MessagingResponse()
		
		#Add a Message
		resp.message(data1)
		
		return str(resp)

if __name__ == "__main__":
    app.run(debug=True)