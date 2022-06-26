import json
import pymongo
import pandas as pd
import re
import urllib3
link = "https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?zip=98006&showNegotiable=true&sortDir=ASC&sourceContext=carGurusHomePageModel&distance=50&sortType=DEAL_SCORE&entitySelectingHelper.selectedEntity=d2436#resultsPage=2"
#link = "https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?sourceContext=carGurusHomePageModel&entitySelectingHelper.selectedEntity=d2436&zip=98006#resultsPage=4"
http = urllib3.PoolManager()

r = http.request('GET', link, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'})
datastring = str(r.data, "utf-8")

jsonData = re.findall("\"listings\":(.*),\"criteoListingIds\"", datastring)
#jsonData = re.findall("\"featuredListings\":(.*),\"criteoListingIds\"", datastring)
jsonDataObject = json.loads(jsonData[0])

#id makeName carYear mileage price daysOnMarket accidentCount ownerCount

for listing in jsonDataObject:
    print("id:" + str(listing['id']) + " car year:"+ str(listing['carYear'])  + " mileage:"+ str(listing['mileage']) + " price:"+ str(listing['price']) + " daysOnMarket:"+ str(listing['daysOnMarket']) + " accidentCount:"+ str(listing['accidentCount']) + " ownerCount:"+ str(listing['ownerCount']))
print(len(jsonDataObject))

#need transmission