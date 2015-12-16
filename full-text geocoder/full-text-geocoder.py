#full-text-geocoder
#John Spurney
import re 
import os

#Resources folder directory for full-text-geocoder
directory = 'C:\\Users\John\Desktop\HPCGIS\Resources'
#This directory location should contain:
#Your twitter stream data to parse (as a .json or .txt file)
twitterDataName = 'twitter-sample.json'

#Information Variables
tweetProfileLocations = []
locationLengthChange = []

#Useful dictionary of US states and territories
states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
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
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
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
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

#Can make more elegant later
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
        self.city = city.title()
        self.state = state.upper()
        
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
    for location in tweetProfileLocations:
        print location
#Main
textGetTweetProfileLocations(twitterDataName)
locationLengthChange = funnel()
encapsulator()

#Testing area
print "\n"
for num in locationLengthChange:
    print num
