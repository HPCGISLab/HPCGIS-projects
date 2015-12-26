#full-text-geocoder
#John Spurney
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import re 
import os

#Resources folder directory for full-text-geocoder
directory = 'C:\\Users\John\Desktop\HPCGIS\Resources'
#This directory location should contain:
#Your twitter stream data to parse (as a .json or .txt file)
twitterDataName = 'twitter-sample.json'
#A Blank text file to write stuff on
blankFile = 'sample-output.txt'
#The 2015 US census gazetteer file name with the national location coordinates
gazetteer = '2015_Gaz_place_national.txt'
#Name for locationLengthChange graph
barGraph = 'sample-bar-graph.png'
#Information Variables
gazHolder = []
tweetProfileLocations = []
locationLengthChange = []

#Useful dictionary of US states and territories
states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
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
        'MS': 'Mississippi',
        'MT': 'Montana',
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
    #returns NationalLocation's values in a comma separated format
    def prettyWrite(self):
        return self.state + ',' + self.city + ',' + self.latitude + ',' + self.longitude

#Uses the twitter data json file to update tweetProfileLocations with the json library
#TODO:Finish jsonGetTweetProfileLocations
def jsonGetTweetProfileLocations():
    print "UNDER CONSTRUCTION"
    
#Uses the twitter data json file to update tweetProfileLocations with a regular expression
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
        #Gazetteer format: (0:State Initial)-(1:City)-(2:Latitude)-(3:Longitude)
        gazHolder.append([temp[0],(" ".join(temp[3:len(temp)- 8])),temp[len(temp)-2:][0],temp[len(temp)-2:][1]])
    #Gets rid of the useless line from the gazetteer
    del gazHolder[0]
    #Closes the gazetteer file 
    f.close()

#If location found: store lat/lon -- else: remove the specific instance inside tweetProfileLocations
def gazGetLatAndLong():
    global tweetProfileLocations, gazHolder, locationLengthChange
    #Sets the instances latitude and longitude if it finds a 'close enough' match
    for location in tweetProfileLocations:
        for i in range(len(gazHolder)):
            if (location.state == gazHolder[i][0]) and (location.city in gazHolder[i][1]):
                location.latitude = gazHolder[i][2]
                location.longitude = gazHolder[i][3]
                break
    #Removes elements from tweetProfileLocations whose location is still unknown after searching the gazetteer
    for i in range(len(tweetProfileLocations)):
        #Don't have to check for both latitude or longitude
        #Because if the first loop didn't modify the instance then the initialized values should remain the same
        if tweetProfileLocations[i].latitude == 'unknown':
            tweetProfileLocations[i] = ""
    #get's rid of empty strings 
    tweetProfileLocations = filter(None, tweetProfileLocations) 
    #Finds out the new length of tweetProfileLocations after non-matches removed
    locationLengthChange.append(len(tweetProfileLocations))

#This function decides what to output and what to do with the national location data
#TODO:Finish harvest function and save all plots
def harvest(pillColor):
    #Writes gathered data on a blank textfile in a comma-delimited format 
    f = open(os.path.join(directory, blankFile),'r+')
    for location in tweetProfileLocations:
        f.write(location.prettyWrite() + "\n")
    f.close()
    
    #Graph that shows how each of the filters affect tweetProfileLocations
    numFilters = len(locationLengthChange)
    testNames = ['Gaz Match', 'stateInfo 2', 'stateInfo 1', 'No Digits','Not Empty','Total']
    allLengthChange = locationLengthChange[::-1]
    
    fig, ax1 = plt.subplots(figsize=(9, 7))
    plt.subplots_adjust(left=0.115, right=0.88)
    fig.canvas.set_window_title('full-text-geocoder graph')
    pos = np.arange(numFilters) + 0.5
    
    ax1.barh(pos, allLengthChange, align='center', height=0.5, color=pillColor)
    ax1.axis([0, 100, 0, numFilters])
    plt.yticks(pos, testNames)
    ax1.set_title('Filter Impact On tweetProfileLocations')
    ax1.set_xlabel("Number Of Locations",size="small")
    
    ax2 = ax1.twinx()
    ax2.plot([100, 100], [0, numFilters], 'white', alpha=0.1)
    ax2.xaxis.set_major_locator(MaxNLocator(7))
    ax2.xaxis.grid(True, linestyle='--', which='major', color='grey', alpha=0.25)
    plt.plot([50, 50], [0, numFilters], 'grey', alpha=0.25)
    ax2.set_yticks(pos)
    
    labels = []
    percents = []
    #Side data presented in format:(number of locations),(percent of locations remaining after filter applied) 
    for num in allLengthChange:
        percents.append(str(round((float(num) / float(allLengthChange[len(allLengthChange)-1]))*100.00,2))+')')
    for i in range(len(allLengthChange)):
       labels.append(str(allLengthChange[i]) + '(' + percents[i])
   
    ax2.set_yticklabels(labels,size="small")
    ax2.set_ylim(ax1.get_ylim())
    plt.show()
    
    plt.savefig(os.path.join(directory, barGraph), bbox_inches='tight')
    
    #TODO:State found heatmap plot
    #TODO:Plot each individual location

#Main
pill = 'red pill'

if pill == 'red pill':
    textGetTweetProfileLocations(twitterDataName)
    locationLengthChange = funnel()
    encapsulator()
    gazInit()
    gazGetLatAndLong()
    harvest('r')
    
elif pill == 'blue pill':
    jsonGetTweetProfileLocations()

