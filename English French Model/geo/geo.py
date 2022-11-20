# -*- coding: utf-8 -*-
"""
Created on Sun May  1 01:31:22 2022

@author: esprit
"""


import requests

u="https://geo.ipify.org/api/v2/country,city?apiKey=at_4yDCLuOGbrY88j1SEp8S3ZV2ERYfH"

r2=requests.get(u)
data2 =r2.json()
print(data2['location']['city'])
latitude =data2['location']['lat']
longitude = data2['location']['lng']

####################################################################################""""
URL = "https://discover.search.hereapi.com/v1/discover"
#latitude = 33.886917
#longitude = 9.537499
api_key = 'AQnBcOqj_NUk3RxzQgdlD4bJHnz9-U7T13FDSHM4U8A' # Acquire from developer.here.com
query = 'bank'
limit = 15

PARAMS = {
            'apikey':api_key,
            'q':query,
            'limit': limit,
            'at':'{},{}'.format(latitude,longitude)
         } 

# sending get request and saving the response as response object 
r = requests.get(url = URL, params = PARAMS) 
data = r.json()






bankOne = data['items'][0]['title']
bankOne_address =  data['items'][0]['address']['label']
bankOne_latitude = data['items'][0]['position']['lat']
bankOne_longitude = data['items'][0]['position']['lng']


bankTwo = data['items'][1]['title']
bankTwo_address =  data['items'][1]['address']['label']
bankTwo_latitude = data['items'][1]['position']['lat']
bankTwo_longitude = data['items'][1]['position']['lng']

bankThree = data['items'][2]['title']
bankThree_address =  data['items'][2]['address']['label']
bankThree_latitude = data['items'][2]['position']['lat']
bankThree_longitude = data['items'][2]['position']['lng']


bankFour = data['items'][3]['title']
bankFour_address =  data['items'][3]['address']['label']
bankFour_latitude = data['items'][3]['position']['lat']
bankFour_longitude = data['items'][3]['position']['lng']

bankFive = data['items'][4]['title']
bankFive_address =  data['items'][4]['address']['label']
bankFive_latitude = data['items'][4]['position']['lat']
bankFive_longitude = data['items'][4]['position']['lng']


from flask import Flask,render_template,jsonify
# from flask_simple_geoip import SimpleGeoIP

app = Flask(__name__)

@app.route('/')

def map_func():
    
	return render_template('map.html',
    			latitude=latitude,
                            longitude=longitude,
                            apikey=api_key,
                            oneName=bankOne,
                            OneAddress=bankOne_address,
                            oneLatitude=bankOne_latitude,
                            oneLongitude=bankOne_longitude,
                            twoName=bankTwo,
                            twoAddress=bankTwo_address,
                            twoLatitude=bankTwo_latitude,
                            twoLongitude=bankTwo_longitude,
                            threeName=bankThree,
                            threeAddress=bankThree_address,
                            threeLatitude=bankThree_latitude,
                            threeLongitude=bankThree_longitude,
                            fourName=bankFour,		
                            fourAddress=bankFour_address,
                            fourLatitude=bankFour_latitude,
                            fourLongitude=bankFour_longitude,
                            fiveName=bankFive,		
                            fiveAddress=bankFive_address,
                            fiveLatitude=bankFive_latitude,
                            fiveLongitude=bankFive_longitude)

if __name__ == '__main__':
	app.run(host="25.75.41.18", port=5000, debug = False)
    
