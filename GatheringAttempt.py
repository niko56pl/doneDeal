import requests
from bs4 import BeautifulSoup

headers = {}
headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.3"
soup = BeautifulSoup(requests.get(url, headers = headers).text, "html.parser")

r = requests.get('https://www.donedeal.ie/cars/Ford/C-MAX')

c = r.content

soup = BeautifulSoup(c, 'lxml')

#main_content = soup.findAll('p', attrs = {'class': 'card__price'})