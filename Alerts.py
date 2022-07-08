import smtplib
from email.message import EmailMessage
import urllib3
import psycopg2
import urllib.parse as up
import pandas as pd
import json
from datetime import date
def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    

    user = 'nathan.project.alerts@gmail.com'
    msg['from'] = user
    password = ''

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()

if __name__ == '__main__':
    maxPrice = 30000
    maxMiles = 50000
    cred = json.load(open('PSQLCredentials.json'))
    url = up.urlparse(cred[0]['connString'])
    conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port )
    cursor  = conn.cursor()

    cursor.execute("select count(*) from listings where insertdate = current_date")
    cursor.execute("select * from listings where insertdate = current_date")
    conn.commit()
    newListings = cursor.fetchall()
    df = pd.DataFrame(newListings)
    numOfNewListings = len(df)
    
    #print(df.loc[df[1]==2018])
    emailBody = f"There are {numOfNewListings} new listings today: \n\n"
    featuredCount = 0
    listings = []
    featured = []
    listings.append(emailBody)
    for i in range(0, numOfNewListings):
        listString = ""
        id = df[0][i]
        print(id)
        year = df[1][i]
        mileage = df[2][i]
        price = df[3][i]
        transmission = df[7][i]
        color = df[8][i]
        maker = df[10][i]

        listString += f"\n\t{year} {maker} for ${price:,}"
        listString += f"\n\t\tDetails:"
        listString += f"\n\t\t\tMileage: {mileage}"
        listString += f"\n\t\t\tTransmission: {transmission}"
        listString += f"\n\t\t\tColor: {color}\n\n"
        listings.append(listString)

        if mileage < maxMiles and price < maxPrice:
            listString = ""
            id = df[0][i]
            
            year = df[1][i]
            mileage = df[2][i]
            price = df[3][i]
            transmission = df[7][i]
            color = df[8][i]
            maker = df[10][i]
            if maker == "Subaru":
                link = "https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?sourceContext=carGurusHomePageModel&entitySelectingHelper.selectedEntity=d2134&zip=98006#listing=" + str(id) 
            else:
                link = "https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?zip=98006&showNegotiable=true&sortDir=ASC&sourceContext=carGurusHomePageModel&distance=50&sortType=DEAL_SCORE&entitySelectingHelper.selectedEntity=d2436#listing=" + str(id)
            listString += f"\n\t{year} {maker} for ${price:,}"
            listString += f"\n\t\tDetails:"
            listString += f"\n\t\t\tMileage: {mileage}"
            listString += f"\n\t\t\tTransmission: {transmission}"
            listString += f"\n\t\t\tColor: {color}\n\n"
            listString += f"\n\tHere is the Link:\n\t" + link 
            featured.append(listString)
            featuredCount += 1
        
    cursor.close()
    conn.close()

    featuredBody = f"There is {featuredCount} listing(s) that are below ${maxPrice} and {maxMiles} miles.\n"
    partition = "_______________________________________________\n"
    listings.insert(0, featuredBody)
    listings.insert(1, " ".join(featured))
    listings.insert(2, partition)
    emailBody = " ".join(listings)
   
    
    emailSubject = str(date.today()) + " Listing Alerts"


    email_alert(emailSubject, emailBody, 'nathanhung369@outlook.com')
