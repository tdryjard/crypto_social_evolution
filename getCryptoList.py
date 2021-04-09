# import libraries
from bs4 import BeautifulSoup
import urllib.request
import csv


cryptos = []

# specify the url
urls = ['https://www.stelareum.io/overview.html', 'https://www.stelareum.io/overview/2.html',
'https://www.stelareum.io/overview/3.html', 'https://www.stelareum.io/overview/4.html',
'https://www.stelareum.io/overview/5.html', 'https://www.stelareum.io/overview/6.html',
'https://www.stelareum.io/overview/7.html', 'https://www.stelareum.io/overview/8.html',
'https://www.stelareum.io/overview/9.html', 'https://www.stelareum.io/overview/10.html']

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

headers={'User-Agent':user_agent,}

for indexUrl, url in enumerate(urls):
    request=urllib.request.Request(url,None,headers) #The assembled request
    page = urllib.request.urlopen(request)
    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(page, 'html.parser')

    # find results within div
    divs = soup.find_all('tr')
    
    nocryptos = []

    for index, div in enumerate(divs):
            textCours = div.find('span', attrs={"class" : "percent_history"})
            price = div.find('span', attrs={"class" : "exchange_rate"})
            a = div.find('a')
            if a and a.get('href') and 'overview' not in a.get('href') and len(a.get('href').replace('/currency/', '').replace('.html', '')) > 2:
                cryptos.append(str(index+(50*indexUrl))+','+a.get('href').replace('/currency/', '').replace('.html', '')+','+str(textCours.getText())+','+str(price.getText().replace(',', '')))


# Create csv and write rows to output file
with open('./csv/crypto-list.csv','w', newline='') as f_output:
    csv_output = csv.writer(f_output, delimiter=",")
    csv_output.writerows([x.split(',') for x in cryptos])