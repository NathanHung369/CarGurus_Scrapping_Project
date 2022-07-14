from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)
#route for index
@app.route('/')
def Index():
    return render_template("index.html")
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
    if request.method == 'POST':
        multiply = float(request.form['multiply'])
        result = multiply*2
        
        return redirect(url_for("success", results = result))


#refresh with answer
@app.route('/success/<int:results>')
def success(results):
    return render_template('showPrice.html', resultPrice= results)


if __name__ == "__main__":
    app.run(debug = True)
