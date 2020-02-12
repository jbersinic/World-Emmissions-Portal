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
app = Flask(__name__)

#################################################
# Database Setup
#################################################


#import psycopg2

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect

engine=create_engine('postgres://xxhcvwyyptnkol:faec1e742584a3c4ad90e01482e3119dccef2a50c2ceb90d1635ef662382c64a@ec2-3-231-46-238.compute-1.amazonaws.com:5432/dblrsk2tqik98a')
connection = engine.connect()
inspector = inspect(engine)
Base = automap_base()
Base.prepare(engine, reflect=True)
#Base.classes.keys()
Emissions = Base.classes.raw_data
#inspector.get_table_names()
raw_data_columns = inspector.get_columns('raw_data')
#for column in raw_data_columns : print(column['name'], column['type'])

''' below is the DB structure'''
#-----------------#
'''sector VARCHAR(120)
indicator VARCHAR(120)
unit VARCHAR(120)
country_code VARCHAR(120)
country VARCHAR(120)
year VARCHAR(120)
variable VARCHAR(120)
value VARCHAR(120)'''
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')
#db = SQLAlchemy(app)

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

# for the graph on Country page
@app.route("/api/emission/<grabcountry>/<grabindicator>")
def countrygraph(grabcountry,grabindicator):
    session = Session(engine)
    results = session.query(Emissions.indicator, Emissions.unit,Emissions.country,Emissions.year,Emissions.value).\
        filter(grabindicator == Emissions.indicator).\
        filter(grabcountry == Emissions.country).all()

    emission_data = [{
        "indicator": results[0],
        "unit": results[1],
        "country": results[2],
        "year": results[3],
        "value": results[4],
    }]

    return jsonify(emission_data)

# for the World graph on Home page 
@app.route("/api/emission/World/<grabindicator>")
def worldgraph(grabindicator):
    session = Session(engine)
    results = session.query(Emissions.indicator, Emissions.unit,Emissions.country,Emissions.year,Emissions.value).\
        filter(grabindicator == Emissions.indicator).\
        filter("World" == Emissions.country).all()

    emission_data = [{
        "indicator": results[0],
        "unit": results[1],
        "country": results[2],
        "year": results[3],
        "value": results[4],
    }]

    return jsonify(emission_data)

# for the World Map on the Home page 
@app.route("/api/emission/wholeworld/<grabyear>/<grabindicator>")
def worldmap (grabyear,grabindicator):
    session = Session(engine)
    results = session.query(Emissions.indicator, Emissions.unit,Emissions.country,Emissions.year,Emissions.value).\
        filter(grabyear == Emissions.year).\
        filter(grabindicator == Emissions.indicator).all()

    emission_data = [{
        "indicator": results[0],
        "unit": results[1],
        "country": results[2],
        "year": results[3],
        "value": results[4],
    }]

    return jsonify(emission_data)


if __name__ == "__main__":
    app.run()
