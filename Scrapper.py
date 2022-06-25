import json
import pymongo
import pandas as pd
import re
import urllib3

link = "https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?sourceContext=carGurusHomePageModel&entitySelectingHelper.selectedEntity=d2436&zip=98006"
http = urllib3.PoolManager()

r = http.request('GET', link, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'})
datastring = str(r.data, "utf-8")
prices = re.findall("<span class=\"price\">\n\s*<span>\$(.*)<\/span>", datastring)
for price in prices:
    price = price.replace(",", "")
    print(price)
hi 
want to roll back
#Nathan's comment