#full-text geocoder
#This full-text takes in metadata that corresponds to the twitter user profile location and returns a latitude and longitude
#John Spurney
#Uses python 3.5

import os
import re 
import urllib.request
import json

#Placeholder strings
sampleCity = "Kent"
sampleState = "OH"

#Like googleGetLatAndLong takes in strings city/state and gets the latitude and longitude
def gazetteerGetLatAndLong(city,state):
	f = open(os.path.join(direct,'2015_Gaz_place_national.txt'),'r')
	
	data = f.read()
	
	pattern = sampleState + "\t\d*\t\d*\t"+ sampleCity + "\D*\d*\t\D\t\d*\t\d*\t*\s*\d*\D\d*\s*\d*\D\d*\t\s(.*?)\n"

	tempTest = re.findall(pattern, data)

	coordinatesContainer = tempTest[0]

	INTPTLAT = re.findall('(.*?)\t', coordinatesContainer)
	INTPTLONG = re.findall('\t\s(.*?)\s', coordinatesContainer)

	latitude = INTPTLAT[0]
	longitude = INTPTLONG[0]

	print("latitude: " + latitude)
	print("longitude " + longitude)

	f.close()


#This function takes a the string with the raw location, and two lists it will modify 
def rawLocationSeparator(locationString,cityHolder,stateHolder):
	commaCounter = 0
	#This loop separates the city and state into two separate lists city and state
	for letter in locationString:
		if letter == ',':
			commaCounter += 1
		elif commaCounter != 1:
			cityHolder.append(letter)
		elif (commaCounter == 1) and (letter != ' '):
			stateHolder.append(letter)

#This function takes a list with characters and concatenates them, returns a string 
def listToString(tmpList):
	tmpString = ""
	for char in tmpList:
		tmpString += char
	tmpString = '"' + tmpString + '"'
	return tmpString

#This function takes in a city, state and the place holders for latitude/longitude string and gets the latitude and longitude 
#Google APIs version
def googleGetLatAndLong(city,state):
# Declares the url string I will be modifying and below it the url that has the latitude and longitude data
	rawUrl = "https://maps.googleapis.com/maps/api/geocode/json?address={city},{state}"
	url = rawUrl[:59] + city + "},{" + state + "}"
	
	class MyOpener(FancyURLopener):
		#User agent string
		version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
	myopener = MyOpener()
	response = myopener.open(url)
	
	content = response.read()
	data = json.loads(content.decode("utf8"))

	latitude = json.dumps([item['geometry']['location']['lat'] for item in data['results']])
	longitude = json.dumps([item['geometry']['location']['lng'] for item in data['results']])

	latitude = latitude[1:-1]
	longitude = longitude[1:-1]
	print("latitude: " + latitude)
	print("longitude " + longitude)

#Takes a string "city, state" and prints the latitude/longitude
def singleLocationOutput(tempString):
	#Declares useful variables
	cityHolder = []
	stateHolder = []
	city = ""
	state = ""
	
	print("")
	print(tempString)
	rawLocationSeparator(tempString,cityHolder,stateHolder)
	city = listToString(cityHolder)
	state = listToString(stateHolder)
	
	#comment/uncomment depending on which one you want to use
	
	#googleGetLatAndLong
	#googleGetLatAndLong(city,state)
	#gazetteerGetLatAndLong
	gazetteerGetLatAndLong(city,state)
	print("")
	
	#Cleans the city/state holder lists
	cityHolder = []
	stateHolder = []

"""Start of tweet parsing"""
direct = 'C:\\Users\John\Desktop\HPCGIS\Resources'
rawFile = open(os.path.join(direct, 'twitter-sample.json'),'r')
blankFile = open(os.path.join(direct,'funnelledLocations.txt'),'r+')

data = rawFile.read()

#Finds the profile locations following twitters pattern with regular expressions 
tweetProfileLocations = re.findall(r'"location": "(.*?)"',data)
UnitedStatesCitiesAndStates = []

#funnels out the locations without commas
tweetProfileLocations = [x for x in tweetProfileLocations if "," in x]

#Gets the targetted locations to geocode, this works because US states have two characters after their city
for loc in tweetProfileLocations:
	tempCityVerifier = []
	cityStart = loc.index(',') + 2
	tempCityVerifier.append(loc[cityStart:])
	for city in tempCityVerifier:
		if len(city) == 2:
			UnitedStatesCitiesAndStates.append(loc)

#Writes the cities that we want our program to geocode onto a text file 
for item in UnitedStatesCitiesAndStates:
	blankFile.write(item + "\n")

print("found " + str(len(UnitedStatesCitiesAndStates)) + " US locations with their city and state.")

rawFile.close()
blankFile.close()
"""End of tweet parsing"""

"""Main Program/Testing Area"""

#A list of strings with the location info
tempLocationsList = []

#Reads locations separated by a new line from a text file and stores them in tempLocationsList
with  open(os.path.join(direct,'funnelledLocations.txt'),'r') as f:
	tempLocationsList = [x.strip() for x in f.readlines()]
f.close()

#Makes sure that for every location in tempLocationsList it prints its location and coordinates
for loc in tempLocationsList:
	singleLocationOutput(loc)

"""End of Main Program/Testing Area"""

#'Notes' text file in temp folder
