# The first line says that we'll use Flask to render a template, redirecting to another url, and creating a URL.
from flask import Flask, render_template, redirect, url_for

# we'll use PyMongo to interact with our Mongo database.
from flask_pymongo import PyMongo

# we will use the scraping code, we will convert from Jupyter notebook to Python.
import scraping