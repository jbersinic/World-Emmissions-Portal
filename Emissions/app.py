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
app = Flask(__name__, static_url_path='/static')

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
Emissions = Base.classes.raw_data2
#inspector.get_table_names()
raw_data_columns = inspector.get_columns('raw_data2')
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
# create route that renders country.html template
@app.route("/country")
def country():
    return render_template("/country.html")
# create route that renders insights.html template
@app.route("/insights")
def insights():
    return render_template("/insights.html")
# create route that renders data.html template
@app.route("/data")
def data():
    return render_template("/data.html")
@app.route("/articles")
def articles():
    return render_template("/articles.html")
# create route that gets all the data
@app.route("/alldata")
def alldata():
    session = Session(engine)
    results = session.query(Emissions.indicator,Emissions.country,Emissions.year).all()
    indicator=[]
    country=[]
    year=[]
    for i in results:
        indicator.append(i[0])
        country.append(i[1])
        year.append(i[2])
    indicator = list( dict.fromkeys(indicator))
    country = list( dict.fromkeys(country))
    year = list( dict.fromkeys(year))
    emission_data = [{
        "indicator": indicator,
        "country": country,
        "year": year,
    }]
    return jsonify(emission_data)
# for the graph on Country page
@app.route("/api/emission/<grabcountry>/<grabindicator>")
def countrygraph(grabcountry,grabindicator):
    session = Session(engine)
    results = session.query(Emissions.indicator, Emissions.unit,Emissions.country,Emissions.year,Emissions.value,Emissions.variable).\
        filter(grabindicator == Emissions.indicator).\
        filter(grabcountry == Emissions.country).all()

    indicator=[]
    unit=[]
    country=[]
    year=[]
    value=[]
    variable=[]
    for i in results:
        indicator.append(i[0])
        unit.append(i[1])
        country.append(i[2])
        year.append(i[3])
        value.append(i[4])
        variable.append(i[5])

    emission_data = [{
        "indicator": indicator,
        "unit": unit,
        "country": country,
        "year": year,
        "value": value,
        "variable":variable
    }]

    return jsonify(emission_data)

# for the World graph on Home page 
@app.route("/api/emission/World/<grabindicator>")
def worldgraph(grabindicator):
    session = Session(engine)
    results = session.query(Emissions.indicator, Emissions.unit,Emissions.country,Emissions.year,Emissions.value).\
        filter(grabindicator == Emissions.indicator).\
        filter("World" == Emissions.country).all()

    indicator=[]
    unit=[]
    country=[]
    year=[]
    value=[]
    for i in results:
        indicator.append(i[0])
        unit.append(i[1])
        country.append(i[2])
        year.append(i[3])
        value.append(i[4])


    emission_data = [{
        "indicator": indicator,
        "unit": unit,
        "country": country,
        "year": year,
        "value": value
    }]

    return jsonify(emission_data)

# for the World Map on the Home page 
@app.route("/api/emission/wholeworld/<grabyear>/<grabindicator>")
def worldmap (grabyear,grabindicator):
    session = Session(engine)
    results = session.query(Emissions.indicator, Emissions.unit,Emissions.country,Emissions.year,Emissions.value).\
        filter(grabyear == Emissions.year).\
        filter(grabindicator == Emissions.indicator).all()
    indicator=[]
    unit=[]
    country=[]
    year=[]
    value=[]
    for i in results:
        indicator.append(i[0])
        unit.append(i[1])
        country.append(i[2])
        year.append(i[3])
        value.append(i[4])


    emission_data = [{
        "indicator": indicator,
        "unit": unit,
        "country": country,
        "year": year,
        "value": value
    }]

    return jsonify(emission_data)

@app.route("/api/news/<grabyear>/<grabcountry>")
def news (grabyear,grabcountry):

    import requests
    from bs4 import BeautifulSoup as b
    import pandas as pd
    import webbrowser

    Country = grabcountry
    Before = grabyear
    url = f"https://www.google.co.in/search?q=+{Country}+co2+emissions+scholarly+articles+before:+{Before}"
    print (url)
    response = requests.get(url)

    soup = b(response.text,"lxml")
    articles=[]
    r = soup.find_all('div', attrs = {'class': 'BNeawe vvjwJb AP7Wnd'})
    for i in range(len(r)):
        articles.append(r[i].text)

    urls = soup.find_all('div', attrs = {'class': 'kCrYT'})
    Links=[]
    for link in urls:
        href = link.find('a')
        try:
            raw_website = href.get('href')
            clean_web = raw_website[7:]
            Links.append(clean_web)
        except:
            continue
    newsdata = [{
        "articles": articles,
        "links": Links
    }]
    return jsonify(newsdata)

if __name__ == "__main__":
    app.run()
