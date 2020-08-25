from __future__ import print_function
import requests
import re
import locale
import time
from time import sleep
from random import randint
from currency_converter import CurrencyConverter
c = CurrencyConverter()
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date, datetime, timedelta
import mysql.connector
import numpy as np
import itertools

locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) # sets the single local language and format
# d = {'€':1,'£':1.2}

# pages = np.arange(0, 58, 29)

entered = datetime.now() # takes the current time and date for insertion into the database

make_model = { # list of makes and models. This should include each one from DoneDeal, however for testing purposes it was kept small.
    #'Abarth': ['500', '595'],
    'Ford': ['C-MAX', 'Focus'],
    'Audi':  ['A3', 'A4']
}

base_url = "https://www.donedeal.ie/cars/"
# "https://www.donedeal.ie/cars/{}/{}"

def insertvariablesintotable(make, model, year, liter, fuel, price, entered): # this function is to establish a connection with the database and input values into the table
    try:
        cnx = mysql.connector.connect(user='root', password='', database='FYP', host='127.0.0.2', port='8000') # credentials
        cursor = cnx.cursor()

        cursor.execute('CREATE TABLE IF NOT EXISTS donedeal ( make VARCHAR(15), model VARCHAR(20), '
                       'year INT(4), liter VARCHAR(3), fuel VARCHAR(6), price INT(6), entered TIMESTAMP) ') # table columns

        insert_query = """INSERT IGNORE INTO donedeal (make, model, year, liter, fuel, price, entered) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        record = (make, model, year, liter, fuel, price, entered)

        cursor.execute(insert_query, record)

        cnx.commit()

    finally:
        if (cnx.is_connected()):
            cursor.close()
            cnx.close()

price_list = [] # store prices here
details_list = [] # and details like year, liter, fuel there

for make in make_model:
    for model in make_model[make]:
        for response in range(0,56,28): # goes through first 2 pages for ads. 28 stands for number of ads to scrape and 56 is to go up as far as end of second page
        #for response in itertools.count(step=30):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            response = requests.get(base_url + make + "/" + model + "?start=" + str(response), headers=headers)

            soup = BeautifulSoup(response.text, 'html.parser')

            #queryURLS = []
            # PULL THE 1st card-collection from the page as there is a 2nd with advertisments.
            # More info on regex to be found below
            # https://stackoverflow.com/questions/499345/regular-expression-to-extract-url-from-an-html-link

            count = 0
            sumTot = 0

            cnx = mysql.connector.connect(user='root', password='', database='FYP', host='127.0.0.2', port='8000')
            cursor = cnx.cursor()

            for details in soup.findAll('ul', attrs={'class': 'card__body-keyinfo'}): # for getting the details from the ad
                #sleep(randint(2, 5))

                if count == 30:
                    break  # ends the for loop

                details = details.text # converts scraped data to a more readable format
                #print(details)
                year = details[:4]
                liter = details[4:7]
                fuel = details[8:14] #exludes electric which has 2 extra
                mileage = re.findall("[0-9]*,[0-9][0-9][0-9]..." , details)
                mileage = ''.join(mileage)
                mileage = mileage.replace(",", "")
                if "mi" in mileage: # converts any ads that have the car's mileage in miles to kilometers
                    mileage = mileage.rstrip('mi')
                    mileage = round(float(mileage) * 1.609)
                mileage = str(mileage)
                if "km" in mileage:
                    mileage = mileage.rstrip('km')
                mileage = mileage.replace("123" or "1234" or "12345" or "123456", "0")
                #print(year, liter, fuel, mileage)

                details_list.append((year, liter, fuel))  # end of one loop go-through, we append
                count += 1  # updates the count value only when a value is appended to the list

                #insertvariablesintotable(make, model, year, liter, fuel, price, entered)

            count = 0
            for price in soup.findAll('p', attrs={'class': 'card__price'}): # for getting the price from the ad
                #sleep(randint(2, 5)) # for delaying the requests so the server doesn't time the scraper out
                if count == 30:
                    break  # ends the for loop

                price = price.text
                price = price.replace("No Price", "0")
                price = price.replace("123" or "1234" or "12345" or "123456", "0")
                price = price.replace(",","")
                price = price.replace("€", "")

                if "p/m" in price:
                    # price = price[:-3]
                    price = price.rstrip("p/m")
                    price = "0"
                else:
                    price_list.append(price)
                    count += 1

                if "£" in price:
                    price = price.replace("£", "")
                    price = c.convert(price, "GBP", "EUR")
                    price = round(price)
                    price_list.append(price)
                    count += 1  # updates the count value when a value is appended to the list

                #sumTot = sumTot + int(price)
                #if price != "0":
                    #count = count + 1

            #average = round(sumTot/count)
            #print("Total:",sumTot)
            #print("Number of ads:",count)
            #print("Average:", average)

        for i in range(len(price_list)):
            print(
            make,
            model,
            details_list[i][0],
            details_list[i][1],
            details_list[i][2],
            price_list[i],
        )
            insertvariablesintotable(make, model, details_list[i][0], details_list[i][1], details_list[i][2], price_list[i], entered) # appends to the database table

        """
            df = pd.DataFrame({
                'Average': [average],
                'Year': [year],
                'Liter': [liter],
                'Fuel': [fuel],
                'Mileage': [mileage]
                })
            print(df)
        """

            #for tag in soup.findAll('a', href=True, class_="card__link"):
            #    queryURLS.append(tag['href'])
            # print(queryURLS)

            #count = 0
            # Pull data from each of the pages
            #for url in queryURLS:
             #   print(url)
              #  response = requests.get(url, headers=headers)
               # soup = BeautifulSoup(response.content, 'html.parser')
                #file = open("data/car"+str(count)+".html","w")
                #count += 1

               # title = soup.findAll("h1", {"itemprop":"name"})
               # print(title)

                #content = soup.prettify()
                #print(content)
                #file.write(content)
               # file.close()

                #print(soup.prettify())

                #title = soup.findAll("title")
                #print(title)
                #price = soup.findAll("span", {"class" : "price ng-binding"})
                #print(price)
                #county = soup.findAll('span', class_="county-disp ng-binding")

               # print(price)
                #print(county)

               # main-content page-row ng-scope
               # < h1 itemprop = "name" ng-bind-html = "adView.ad.header" class ="ng-binding" > Ford C-Max < / h1 >
               # <span class="county-disp ng-binding">Offaly</span>
               # <span class ="price ng-binding" > 999 < / span >

                #class ="cad-content divider"

                #class="cad-info-container space-top-10"
