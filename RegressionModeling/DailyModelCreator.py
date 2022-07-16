import json
import psycopg2
import urllib.parse as up
import pandas as pd
import urllib3
from datetime import date
import os
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import statsmodels.api as sm
#Connect to Database and convert relevent data into a DataFrame
#Connect to Database
parentDir = os.path.dirname(os.getcwd())
#path = parentDir+'/PSQLCredentials.json'
path = parentDir+'trader33drakor/PSQLCredentials.json'

cred = json.load(open(path))
url = up.urlparse(cred[1]['connString'])
conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port )
cursor  = conn.cursor()
cursor.execute("select * from (select caryear, mileage, model, ownercount, accidentcount, price, Case When transmission like '%Manual%' Then 'Manual' When transmission like '%Automatic%' Then 'Automatic' Else 'Unknown' End transmission from listings where caryear is not null and mileage is not null and transmission is not null and model is not null and accidentcount is not null and ownercount is not null) a where a.transmission != 'Unknown'")
conn.commit()
df = pd.DataFrame(cursor.fetchall())
#Add column names to dataframe
df = df.rename(columns = {0:'Year', 1:'Mileage', 2: 'Maker', 3:'OwnerCount', 4:'AccidentCount', 5:'Price', 6:'Transmission'})
#Convert all numerical data into float
df[["Price"]] = df[["Price"]].apply(pd.to_numeric)
#Create dummy data for categorical data types
df['Maker'] = df['Maker'].map({'Toyota 86': 0, 'Subaru BRZ': 1})
df['Transmission'] = df['Transmission'].map({'Manual': 0, 'Automatic': 1})


#Create model
X = df[['Year', 'Mileage', 'Maker']]
X = sm.add_constant(X)
Y = df[["Price"]]
mod = sm.OLS(Y, X)
res = mod.fit()
model = res.params
print(model)
intercept = model[0]
yearCoef = model[1]
mileageCoef = model[2]
makerCoef = model[3]

#inserts model into database

sql = "Insert into Regression (insertDate, yearCoef, mileageCoef, makerCoef, intercept) VALUES (current_date, %s, %s, %s, %s)"
data = (yearCoef, mileageCoef, makerCoef, intercept)
cursor.execute(sql, data)
conn.commit()
cursor.close()
conn.close()