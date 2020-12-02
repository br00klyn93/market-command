from flask import Flask, request, render_template, redirect
from flask import make_response, Response

import urllib.parse, urllib.request

import requests
from bs4 import BeautifulSoup
import mechanicalsoup
import re
from collections import namedtuple
from enum import Enum

app = Flask(__name__)

# email = "s-mclauryb@bsd405.org"
# password = "Brooklyn611!"

# Definitions
Security = namedtuple("Security", "symbol description quantity purchase_price current_price current_value")
class Duration(Enum):
    day_order = 1
    good_cancel = 2
class Action(Enum):
    buy = 1
    sell = 2
    short = 3
    cover = 4

# Initialize the browser, we only use one for all the methods as I have a feeling you may get deauthed if you dont
browser = mechanicalsoup.StatefulBrowser()

# Login page for the trading game
login_page = browser.open("https://investopedia.com/accounts/login.aspx?returnurl=http://www.investopedia.com/simulator/")

@app.route('/')
def main():
    return('Alive an well.')


@app.route('/status')
def get_portfolio_status():
    email = request.args['email']
    pw = request.args['pw']

    # LOG IN
    home_page = login(email,pw)

    # GETS WHAT WE WANT TO RETURN FROM THE URL
    info_type = request.args['info_type']

    response = browser.open("https://investopedia.com/simulator/portfolio/")
    parsed_html = response.soup

    acct_val_id = "ctl00_MainPlaceHolder_currencyFilter_ctrlPortfolioDetails_PortfolioSummary_lblAccountValue"
    buying_power_id = "ctl00_MainPlaceHolder_currencyFilter_ctrlPortfolioDetails_PortfolioSummary_lblBuyingPower"
    cash_id = "ctl00_MainPlaceHolder_currencyFilter_ctrlPortfolioDetails_PortfolioSummary_lblCash"
    return_id = "ctl00_MainPlaceHolder_currencyFilter_ctrlPortfolioDetails_PortfolioSummary_lblAnnualReturn"

    # Use BeautifulSoup to extract the relevant values based on html ID tags
    account_value = parsed_html.find('span', attrs={'id': acct_val_id}).text
    buying_power = parsed_html.find('span', attrs={'id': buying_power_id}).text
    cash = parsed_html.find('span', attrs={'id': cash_id}).text
    annual_return = parsed_html.find('span', attrs={'id': return_id}).text

    # We want our returned values to be floats
    # Use regex to remove non-numerical or decimal characters
    # But keep - (negative sign)
    regexp = "[^0-9.-]"
    account_value = float(re.sub(regexp, '', account_value))
    buying_power = float(re.sub(regexp, '', buying_power))
    cash = float(re.sub(regexp, '', cash))
    annual_return = float(re.sub(regexp, '', annual_return))

    return(info_type)


def login(user,pass):
    #Elements of the login page form
    login_form = login_page.soup.select("form")[0]
    login_form.select("#username")[0]["value"] = email
    login_form.select("#password")[0]["value"] = password
    home_page = browser.submit(login_form, login_page.url)

    # MAYBE AN ISSUE?
    return(home_page)



if __name__ == "__main__":
    app.run("0.0.0.0",port=5000)
