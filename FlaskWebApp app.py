
from flask import Flask, render_template, url_for, request, redirect
import os
import json
import psycopg2
import urllib.parse as up
from flask_talisman import Talisman
import smtplib
from email.message import EmailMessage



app = Flask(__name__)
Talisman(app, content_security_policy=None)
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

#route for Jupyter Notebook
@app.route('/Project/Jupyter')
def Jupyter():
    return render_template("Jupyter.html")


#route for Resume
@app.route('/Resume')
def Resume():
    return render_template("Resume.html")

#route for Linkedin
@app.route('/github')
def github():
    return render_template("linkedIn.html")

#route for Contact
@app.route('/Contact', methods=['POST', 'GET'])
def Contact():

    def email_alert(subject, body, to):
        msg = EmailMessage()
        msg.set_content(body)
        msg['subject'] = subject
        msg['to'] = to
        

        user = 'nathan.project.alerts@gmail.com'
        msg['from'] = user
        password = 'okjgfadmakfznaaq'


        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(user, password)
        server.send_message(msg)
        server.quit()


    if request.method == 'POST':
        name = request.form['Name']
        email = request.form['Email']
        message = request.form['Message']
        print(name)
        print(email)
        print(message)
        emailSubject = f"{name} emailed you from website"
        emailBody = f"Name: {name} \nEmail: {email} \nMessage: {message}"
        print(emailSubject)
        print(emailBody)
        email_alert(emailSubject, emailBody, 'nathanhung369@outlook.com')
    return render_template("Contact.html")



#route for submit
@app.route('/submit', methods=['POST', 'GET'])
def submit():

    #Connect to Database and convert relevent data into a DataFrame
    #Connect to Database
    parentDir = os.path.dirname(os.getcwd())
    
    #path = parentDir+'\PSQLCredentials.json'
   
    path = ("PSQLCredentials.json")


    cred = json.load(open(path))
    url = up.urlparse(cred[1]['connString'])
    conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port )
    cursor  = conn.cursor()
    cursor.execute("select * from regression order by modelid desc limit 1")
    conn.commit() 
    data = cursor.fetchall()
    yearcoef = float(data[0][2])
    mileagecoef = float(data[0][3])
    makercoef = float(data[0][4])
    intercept = float(data[0][5])

    if request.method == 'POST':
        year = float(request.form['Year'])#searches form with Name
        mileage = float(request.form['Mileage'])
        maker = 0
        if(str(request.form['Maker'])== 'Toyota'):
            maker = float(0)
        else:
            maker = float(1)
        
        result = (yearcoef * year) + (mileagecoef * mileage) + (maker * makercoef)+ intercept
        print(result)
        print(year)
        print(mileage)
        print((mileagecoef))
        return redirect(url_for("success", price = result, year = year, mileage = mileage, maker = request.form['Maker'] ))


#refresh with answer
@app.route('/Project/Estimator/success/<price>, <year>, <mileage>, <maker>')
def success(price, year, mileage, maker):
    return render_template('ShowPrice.html', price = price, year = str(year), mileage = mileage, maker = maker)


if __name__ == "__main__":
    app.run(debug = False)
