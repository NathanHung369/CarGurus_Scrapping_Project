import json
import psycopg2
import urllib.parse as up
import pandas as pd
import re
import urllib3
link = "https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?zip=98006&showNegotiable=true&sortDir=ASC&sourceContext=carGurusHomePageModel&distance=50&sortType=DEAL_SCORE&entitySelectingHelper.selectedEntity=d2436#resultsPage=2"
http = urllib3.PoolManager()
#Scrape Data and load in JSON object
r = http.request('GET', link, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'})
datastring = str(r.data, "utf-8")
jsonData = re.findall("\"listings\":(.*),\"criteoListingIds\"", datastring)
jsonDataObject = json.loads(jsonData[0])

#Connect to Database
cred = json.load(open('PSQLCredentials.json'))
url = up.urlparse(cred[0]['connString'])
conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port )
cursor  = conn.cursor()

totalOptions = 0

#Inserts data into PSQL data validation tables
for i in range(0, len(jsonDataObject)):
    listing = jsonDataObject[i]
    id = str(listing['id'])
    carYear = str(listing['carYear'])
    mileage = str(listing['mileage'])
    price = str(listing['price'])
    daysOnMarket = str(listing['daysOnMarket'])
    accidentCount = str(listing['accidentCount'])
    ownerCount = str(listing['ownerCount'])
    transmission = str(listing['localizedTransmission'])
    ExteriorColor = str(listing['normalizedExteriorColor'])
    options = listing['options']


    sql = "Insert into DayListings (ListingID, CarYear, Mileage, Price, DaysOnMarket, AccidentCount, OwnerCount, Transmission, ExteriorColor) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (id, carYear, mileage, price, daysOnMarket, accidentCount, ownerCount, transmission, ExteriorColor)
    cursor.execute(sql, data)
    conn.commit()


    for j in range(0, len(options)):
        sql = "Insert into DayOptions (ListingID, Option) VALUES (%s, %s)"
        data = (id, options[j])
        cursor.execute(sql, data)
        conn.commit()
        totalOptions += 1

#Inserts new data into db
cursor.execute("Insert into Listings (listingid, caryear, mileage, price, daysonmarket, accidentcount, ownercount, transmission, exteriorcolor) Select d.listingid, d.caryear, d.mileage, d.price, d.daysonmarket, d.accidentcount, d.ownercount, d.transmission, d.exteriorcolor from DayListings d left outer join Listings l on d.ListingID = l.ListingID;")
conn.commit()
cursor.execute("Insert into Options (OptionID, ListingID, Option) Select d.OptionID, d.ListingID, d.Option from DayOptions d left outer join Options l on d.OptionID = l.OptionID")
conn.commit()
cursor.execute("Delete from DayOptions")
conn.commit()
cursor.execute("Delete from DayListings")
conn.commit()


cursor .close()
conn.close()
print("Inserted "+ str(len(jsonDataObject))+" listings and "+ str(totalOptions) + " options")