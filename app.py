
# import dependencies.
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False) 

# The first line says that we'll use Flask to render a template, redirecting to another url, and creating a URL.
from flask import Flask, render_template, redirect, url_for

# we'll use PyMongo to interact with our Mongo database.
from flask_pymongo import PyMongo

# we will use the scraping code, we will convert from Jupyter notebook to Python.
import scraping

app = Flask(__name__) # Set up Flask

# tell Python how to connect to Mongo using PyMongo.
# Use flask_pymongo to set up mongo connection

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"

# app.config["MONGO_URI"] tells Python that our app will connect to Mongo using a URI, 
# a uniform resource identifier similar to a URL.
# "mongodb://localhost:27017/mars_app" is the URI we'll be using to connect our app to Mongo. 
# This URI is saying that the app can reach Mongo through our localhost server, 
# using port 27017, using a database named "mars_app".

mongo = PyMongo(app)

# define the route for the HTML page.
@app.route("/") # tells Flask what to display when we're looking at the home page, index.html
def index():
   mars = mongo.db.mars.find_one() # uses PyMongo to find the "mars" collection in our database
   return render_template("index.html", mars=mars) # tells Flask to return an HTML template using an index.html

# set up our scraping route. This route will be the "button" of the web application.
@app.route("/scrape") # defines the route that Flask will be using
def scrape():
   mars = mongo.db.mars # assign a new variable that points to our Mongo database: mars = mongo.db.mars.
   mars_data = scraping.scrape_all() # created a new variable to hold the newly scraped data: mars_data = scraping.scrape_all().
   mars.update({}, mars_data, upsert=True) # we've gathered new data, we need to update the database
   return redirect('/', code=302)

if __name__ == "__main__":
   app.debug = True
   app.run()
