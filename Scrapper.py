import json
import psycopg2
import urllib.parse as up
import pandas as pd
import re
import urllib3
from Alerts import email_alert
from datetime import date

def testNull(key):
    try:
        data = carYear = str(listing[key])
    except KeyError:
        data = None
    return data

links = ["https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?zip=98006&showNegotiable=true&sortDir=ASC&sourceContext=carGurusHomePageModel&distance=50&sortType=DEAL_SCORE&entitySelectingHelper.selectedEntity=d2436#resultsPage=2", "https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?sourceContext=carGurusHomePageModel&entitySelectingHelper.selectedEntity=d2134&zip=98006"]
models = ["Toyota 86", "Subaru BRZ"]
http = urllib3.PoolManager()

#Connect to Database

cred = json.load(open('PSQLCredentials.json'))
#cred = json.load(open('C:/Users/Nathan/source/repos/CarGurus_Scrapping_Project/PSQLCredentials.json'))
for c in range(0, 2):
    print(c)

    url = up.urlparse(cred[c]['connString'])
    conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port )
    cursor  = conn.cursor()
    cursor.execute("Delete from DayOptions")
    conn.commit()
    cursor.execute("Delete from DayListings")
    conn.commit()

    today = date.today()
    totalOptions = 0
    totalListings = 0
    #Scrape Data and load in JSON object
    for k in range(0, len(links)):

        r = http.request('GET', links[k], headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'})
        datastring = str(r.data, "utf-8")
        jsonData = re.findall("\"listings\":(.*),\"criteoListingIds\"", datastring)
        jsonDataObject = json.loads(jsonData[0])

        

        

        #Inserts data into PSQL data validation tables
        for i in range(0, len(jsonDataObject)):
            listing = jsonDataObject[i]
            id = str(listing['id'])
            carYear = testNull('carYear')
            mileage = testNull('mileage')
            price = testNull('price')
            daysOnMarket = testNull('daysOnMarket')
            accidentCount = testNull('accidentCount')
            ownerCount = testNull('ownerCount')
            transmission = testNull('localizedTransmission')
            ExteriorColor = testNull('normalizedExteriorColor')
            options = listing['options'] 
        
            model = models[k]
            

            sql = "Insert into DayListings (ListingID, CarYear, Mileage, Price, DaysOnMarket, AccidentCount, OwnerCount, Transmission, ExteriorColor, Model) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (id, carYear, mileage, price, daysOnMarket, accidentCount, ownerCount, transmission, ExteriorColor, model)
            cursor.execute(sql, data)
            conn.commit()

            totalListings +=1 
            for j in range(0, len(options)):
                sql = "Insert into DayOptions (ListingID, Option) VALUES (%s, %s)"
                data = (id, options[j])
                cursor.execute(sql, data)
                conn.commit()
                totalOptions += 1

        #Inserts new data into db
        
        cursor.execute("Insert into Listings (listingid, caryear, mileage, price, daysonmarket, accidentcount, ownercount, transmission, exteriorcolor, listingdate, model, insertDate) Select d.listingid, d.caryear, d.mileage, d.price, d.daysonmarket, d.accidentcount, d.ownercount, d.transmission, d.exteriorcolor, current_date, d.model, current_date from DayListings d left join Listings l on d.ListingID = l.ListingID where l.ListingID is null;")
        conn.commit()   

        cursor.execute("Insert into Options (OptionID, ListingID, Option) Select d.OptionID, d.ListingID, d.Option from DayOptions d join (Select a.listingid from DayListings a left join Listings b on a.ListingID = b.ListingID where b.ListingID is null) l on d.ListingID = l.ListingID;")
        conn.commit()

        cursor.execute("update listings set daysonmarket = (select daysonmarket from daylistings where listings.ListingID = daylistings.ListingID) From dayListings where Listings.ListingID = dayListings.ListingID")
        conn.commit()
        cursor.execute("update listings set listingdate = current_date-dayListings.daysonmarket From dayListings where Listings.ListingID = dayListings.ListingID")
        conn.commit()
        cursor.execute("Delete from DayOptions")
        conn.commit()
        cursor.execute("Delete from DayListings")
        conn.commit()

    #cursor.execute("update listings set listingdate = current_date-daysonmarket")
    conn.commit()
    cursor .close()
    conn.close()
print("found "+ str(totalListings)+" listings and "+ str(totalOptions) + " options")