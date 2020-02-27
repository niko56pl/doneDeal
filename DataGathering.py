import requests
import re
import locale
from currency_converter import CurrencyConverter
c = CurrencyConverter()
from bs4 import BeautifulSoup
import pandas as pd

locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )
#d = {'€':1,'£':1.2}

url = "https://www.donedeal.ie/cars/Ford/C-MAX"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
response = requests.get(url, headers=headers)

#queryURLS = []
# PULL THE 1st card-collection from the page as there is a 2nd with advertisments.
# More info on regex to be found below
# https://stackoverflow.com/questions/499345/regular-expression-to-extract-url-from-an-html-link

soup = BeautifulSoup(response.text, 'html.parser')
count = 0
sumTot = 0
for price in soup.findAll('p', attrs={'class': 'card__price'}):
    price = price.text
    price = price.replace("No Price", "0")
    price = price.replace(",","")
    price = price.replace("€", "")
    if "p/m" in price:
        #price = price[:-3]
        price = price.rstrip('p/m')
        price = "0"
    if "£" in price:
        price = price.replace("£", "")
        price = c.convert(price, 'GBP', 'EUR')
        price = round(price)

    print(price)

    #currency_only = re.compile(r'£|€')
    #just_currency = currency_only.findall(price)
    #print(just_currency)
    '''
    price_only = re.compile(r'\d[0-9.]+')
    just_price = price_only.findall(price)
    integer_price = int(just_price[0])
    
    #print(integer_price) '''

    sumTot = sumTot + int(price)
    if price != "0":
        count = count + 1
    price = price.replace("0", "")

print("Total:",sumTot)
print("Number of ads:",count)
print("Average:", round(sumTot/count))

#df = pd.DataFrame({'Price': integer_price})
#print(df)

"""
for sterling in price:
    prices = price.contents[0]
    regex_pattern = prices.compile("\d+")
    price_figure = prices
    result = "".join(regex_pattern.findall(price_figure))
    len(price_list)
    print(prices + "\n"]])
    print(result)

"""
#for item in soup.get_text().split():
#    currency = item[0]
#    value = locale.atof(item[1:])
#    k = d[currency]
#    print(currency,value,k*value)

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
