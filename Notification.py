import json
import psycopg2
import urllib.parse as up
import urllib3

#Connect to Database
cred = json.load(open('PSQLCredentials.json'))
url = up.urlparse(cred[0]['connString'])
conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port )
cursor  = conn.cursor()

cursor.execute("update listings set listingdate = current_date-daysonmarket")
conn.commit()

cursor .close()
conn.close()