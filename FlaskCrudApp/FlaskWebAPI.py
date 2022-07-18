from asyncio.windows_events import NULL
from flask import Flask, render_template, url_for, request, redirect
import os
import json
import psycopg2
import urllib.parse as up





app = Flask(__name__)

#route for home
@app.route('/')
def Index():
    return render_template("home.html")

#route for Estimator
@app.route('/Project/Estimator')
def Estimator():
    return render_template("index.html")

#route for Design
@app.route('/Project/Design')
def Design():
    return render_template("design.html")

#route for Dashboard
@app.route('/Project/Dashboard')
def Dashboard():
    return render_template("dashboard.html")


#route for Resume
@app.route('/Resume')
def Resume():
    return render_template("Resume.html")
#route for Linkedin
@app.route('/linkedIn')
def linkedIn():
    return render_template("linkedIn.html")
#route for Contact
@app.route('/Contact')
def Contact():
    return render_template("Contact.html")



#route for submit
@app.route('/submit', methods=['POST', 'GET'])
def submit():

    #Connect to Database and convert relevent data into a DataFrame
    #Connect to Database
    parentDir = os.path.dirname(os.getcwd())
    print(parentDir)
    path = parentDir+'\PSQLCredentials.json'
    #path = parentDir+'/trader33drakor/PSQLCredentials.json'
    cred = json.load(open(path))
    url = up.urlparse(cred[1]['connString'])
    conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port )
    cursor  = conn.cursor()
    cursor.execute("select * from regression order by modelid desc limit 1")
    conn.commit() 
    data = cursor.fetchall()
    yearcoef = int(data[0][2])
    mileagecoef = int(data[0][3])
    makercoef = float(data[0][4])
    intercept = float(data[0][5])

    if request.method == 'POST':
        year = float(request.form['Year'])#searches form with Name
        mileage = float(request.form['Mileage'])
        maker = NULL
        if(str(request.form['Maker'])== 'Toyota'):
            maker = float(0)
        else:
            maker = float(1)
        
        result = (yearcoef * year) + (mileagecoef * mileage) + (maker * makercoef)+ intercept
        
        return redirect(url_for("success", price = result, year = year, mileage = mileage, maker = request.form['Maker'] ))


#refresh with answer
@app.route('/Project/Estimator/success/<price>, <year>, <mileage>, <maker>')
def success(price, year, mileage, maker):
    return render_template('showPrice.html', price = price, year = str(year), mileage = mileage, maker = maker)


if __name__ == "__main__":
    app.run(debug = True)
