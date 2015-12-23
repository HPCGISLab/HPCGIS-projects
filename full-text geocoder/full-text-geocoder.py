#full-text-geocoder
#John Spurney
import re 
import os

#Resources folder directory for full-text-geocoder
directory = 'C:\\Users\John\Desktop\HPCGIS\Resources'
#This directory location should contain:
#Your twitter stream data to parse (as a .json or .txt file)
twitterDataName = 'twitter-sample.json'
#The 2015 US census gazetteer file name with the national location coordinates
gazetteer = '2015_Gaz_place_national.txt'
#Information Variables
gazHolder = []
tweetProfileLocations = []
locationLengthChange = []

#Useful dictionary of US states and territories
#Places not supported by the gazetteer are commented out
states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        #'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        #'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        #'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        #'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        #'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

#Keys and Values individually
stateKeys = states.keys()
stateKeys = [' {0}'.format(elem) for elem in stateKeys] 
stateKeys = [x.lower() for x in stateKeys] 

stateValues = states.values()
stateValues = [' {0}'.format(elem) for elem in stateValues] 
stateValues = [x.lower() for x in stateValues] 

stateInfo = stateKeys + stateValues

#NationaLocation class
#When creating an instance of NationalLocation
#be sure the city and state only have alphabetic characters
class NationalLocation:
    def __init__(self, city, state):
        #string
        self.city = city.title()
        #string
        self.state = state.upper()
        #initialized as string, turns into float later
        self.latitude = 'unknown'
        self.longitude = 'unknown'
    def formalWrite(self):
        return self.city + ', ' + self.state
        
#Uses the twitter data text file to update tweetProfileLocations 
def textGetTweetProfileLocations(fileName):
    global tweetProfileLocations
    streamText = open(os.path.join(directory, fileName),'r')
    data = streamText.read()
    tempProfileLocations = re.findall(r'"location": "(.*?)"',data)
    streamText.close()
    tweetProfileLocations = tempProfileLocations

#Gets rid of not-wanted strings from tweetProfileLocations
def funnel():
    global tweetProfileLocations, stateInfo
    tmp = []
    tmpTweets = []
    #total number of profile locations found
    tmp.append(len(tweetProfileLocations))
    #get's rid of empty strings 
    tweetProfileLocations = filter(None, tweetProfileLocations)
    tmp.append(len(tweetProfileLocations))
    #get's rid of strings with digits
    tweetProfileLocations = [x for x in tweetProfileLocations if not re.search(r'\d',x)]
    tmp.append(len(tweetProfileLocations))
    #Makes all the locations lowercase for easier examination    
    tweetProfileLocations = [x.lower() for x in tweetProfileLocations]  
    #Has any of the elements in stateInfo
    tweetProfileLocations = [i for i in tweetProfileLocations if any(j in i for j in stateInfo)]
    tmp.append(len(tweetProfileLocations))
    #Final inspection filter
    for i in range(len(tweetProfileLocations)):
        for j in range(len(stateInfo)):
            if ((len(tweetProfileLocations[i])) > (len(stateInfo[j]))) and (stateInfo[j][::-1] == tweetProfileLocations[i][::-1][0:len(stateInfo[j])]):
                tmpTweets.append(tweetProfileLocations[i])
                break
    tweetProfileLocations = tmpTweets
    tmp.append(len(tweetProfileLocations))
    #Returns a list with the length of locations after each filter applied
    return tmp

#Organizes the raw profile location strings that made it through the funnel
#and puts them inside NationalLocation containers   
def encapsulator():
    global tweetProfileLocations
    tempSplitLocations = []
    #Splits the city and state
    for i in range(len(tweetProfileLocations)):
        for j in range(len(stateInfo)):
            if ((len(tweetProfileLocations[i])) > (len(stateInfo[j]))) and (stateInfo[j][::-1] == tweetProfileLocations[i][::-1][0:len(stateInfo[j])]):
                tempSplitLocations.append(tweetProfileLocations[i].split(stateInfo[j]))
                #len(stateKeys or stateValues) decides modulo operation outcome
                if j >= len(stateKeys):
                    tempSplitLocations[i][1] = stateInfo[j % len(stateKeys)][1:]
                else:
                    tempSplitLocations[i][1] = stateInfo[j][1:]
                break
    #If a city string has a comma in front of it, this removes the comma
    for i in range(len(tempSplitLocations)):
        if tempSplitLocations[i][0][len(tempSplitLocations[i][0]) - 1:] == ',':
            tempSplitLocations[i][0] = tempSplitLocations[i][0][:-1]
    #Encapsulates the raw location string data
    tweetProfileLocations = []
    for location in tempSplitLocations:
        tweetProfileLocations.append(NationalLocation(location[0],location[1]))


#This extracts the Information I need from the gazetteer
def gazInit():
    global gazHolder
    #Open gazetteer file
    f = open(os.path.join(directory,'2015_Gaz_place_national.txt'),'r')
    #There are 29575 lines of information total in the gazetteer
    #Organizes the relevant information from the gazetteer into a list
    for line in f:
        temp = line.split()
        #Gazetteer format: (State Initial)-(City)-(Latitude)-(Longitude)
        gazHolder.append([temp[0],(" ".join(temp[3:len(temp)- 8])),temp[len(temp)-2:][0],temp[len(temp)-2:][1]])
    #Gets rid of the useless line from the gazetteer
    del gazHolder[0]
    #Closes the gazetteer file 
    f.close()

#Main
textGetTweetProfileLocations(twitterDataName)
locationLengthChange = funnel()
encapsulator()
gazInit()

#Testing area
for location in tweetProfileLocations:
    print location.formalWrite()

print "\n"
for num in locationLengthChange:
    print num
