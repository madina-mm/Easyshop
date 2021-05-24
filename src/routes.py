from src import app
from flask import render_template
from src import forms
from src.business_layer.amazon_scraper import *
from src.business_layer.tapaz_scraper import *


@app.route("/")
@app.route("/home")
@app.route("/about")
def home():
    return render_template("home.html")


@app.route("/search", methods=['GET', 'POST'])
def search():
    '''
    form = SearchForm()
    item = form.item.data
    min_price = form.min_price.data
    max_price = form.max_price.data
    sort_price_option = None
    sort_rating_option = None
    currency = None
    '''
    tapaz_results = tapaz_scraper('iphone 11')
    amazon_results = amazon_scraper('samsung a70')

    return render_template('search.html', tapaz_results=tapaz_results, amazon_results=amazon_results, n=len(tapaz_results), m=len(amazon_results))