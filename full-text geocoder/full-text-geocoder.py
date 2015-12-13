#full-text-geocoder
#John Spurney
import re 
import os

#Resources folder directory for full-text-geocoder
directory = 'C:\\Users\John\Desktop\HPCGIS\Resources'
#This directory location should contain:
#Your twitter stream data to parse (for now as a .txt file)
twitterDataName = 'twitter-sample.txt'

#Information Variables
tweetProfileLocations = []
filterChanges = []

#Uses the twitter data text file to update tweetProfileLocations 
def textGetTweetProfileLocations(fileName):
    global tweetProfileLocations
    streamText = open(os.path.join(directory, fileName),'r')
    data = streamText.read()
    tempProfileLocations = re.findall(r'"location": "(.*?)"',data)
    streamText.close()
    tweetProfileLocations = tempProfileLocations

#Gets rid of not-wanted strings from tweetProfileLocations
def funnelLocations():
    global tweetProfileLocations
    tmp = []
    #total number of profile locations found
    tmp.append(len(tweetProfileLocations))
    #Filter 1, get's rid of empty strings 
    tweetProfileLocations = filter(None, tweetProfileLocations)
    tmp.append(len(tweetProfileLocations))
    #Returns a list with the length of locations after each filter applied
    return tmp
    
#Main
textGetTweetProfileLocations(twitterDataName)
filterChanges = funnelLocations()

#Prints for testing
print "---------------"
for num in filterChanges:
    print num




