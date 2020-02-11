# import necessary libraries
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#################################################
# Flask Setup
#################################################
app = Flask(__name__,
            template_folder="templates")

#################################################
# Database Setup
#################################################

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')
db = SQLAlchemy(app)

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("/index.html")
# create route that renders country.html template
@app.route("/country")
def country():
    return render_template("/country.html")
# create route that renders insights.html template
@app.route("/insights")
def insights():
    return render_template("/insights.html")

# Query the database and send the jsonified results
@app.route("/send", methods=["GET", "POST"])
def send():
    #if request.method == "POST":
        #name = request.form["petName"]
        #lat = request.form["petLat"]
        #lon = request.form["petLon"]

        #pet = Pet(name=name, lat=lat, lon=lon)
        #db.session.add(pet)
        #db.session.commit()
        #return redirect("/", code=302)

    #return render_template("form.html")

if __name__ == "__main__":
    app.run(debug = True)
