# import libraries
from bs4 import BeautifulSoup
import urllib.request
import csv
import getCryptoListCsv
import getCryptoList
import getNegativeWord
import getPositiveWord
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys




# specify the url

urlsB = ['https://www.reddit.com/r/CryptoCurrency/rising/', 'https://www.reddit.com/r/CryptoCurrency/new/',
'https://www.reddit.com/r/CryptoMoonShots/', 'https://www.reddit.com/r/CryptoMoonShots/new/',
'https://www.reddit.com/r/CryptoMoonShots/top/', 'https://www.reddit.com/r/CryptoCurrencies/',
'https://www.reddit.com/r/CryptoCurrencies/new/', 'https://www.reddit.com/r/CryptoCurrencies/top/',
'https://www.reddit.com/r/crypto/', 'https://www.reddit.com/r/crypto/new/', 'https://www.reddit.com/r/crypto/top/',
'https://www.reddit.com/r/investing/', 'https://www.reddit.com/r/investing/new/', 'https://www.reddit.com/r/investing/top/',
'https://www.reddit.com/r/binance/', 'https://www.reddit.com/r/binance/new/', 'https://www.reddit.com/r/binance/top/', 'https://www.reddit.com/r/SatoshiStreetBets/hot/',
'https://www.reddit.com/r/SatoshiStreetBets/new/', 'https://www.reddit.com/r/SatoshiStreetBets/top/',
'https://www.reddit.com/r/Crypto_Currency_News/', 'https://www.reddit.com/r/Crypto_Currency_News/new/',
'https://www.reddit.com/r/CryptoMarkets/', 'https://www.reddit.com/r/CryptoMarkets/new/',
'https://www.reddit.com/r/CryptoMarkets/top/']

url_test = ['https://www.reddit.com/r/CryptoCurrency/rising/']

urlsNews = ['https://www.reddit.com/r/CryptoCurrency/new/','https://www.reddit.com/r/CryptoMoonShots/new/',
'https://www.reddit.com/r/CryptoCurrencies/new/','https://www.reddit.com/r/crypto/new/', 'https://www.reddit.com/r/investing/new/',
'https://www.reddit.com/r/binance/new/', 'https://www.reddit.com/r/SatoshiStreetBets/new/',
'https://www.reddit.com/r/Crypto_Currency_News/new/', 'https://www.reddit.com/r/Crypto_Currency_News/top/',
'https://www.reddit.com/r/CryptoMarkets/new/']

while 10:

    titles = []
    dates = []
    comments = []
    stats = [0] * len(getCryptoListCsv.cryptos)
    negativeWordCount = [0] * len(getCryptoListCsv.cryptos)
    positiveWordCount = [0] * len(getCryptoListCsv.cryptos)
    nbComments = [0] * len(getCryptoListCsv.cryptos)

    urlUse = 'urls-B'

    for url in urlsNews:

        browser = webdriver.Safari()
        # IF NO SAFARI BROWSER :
        # browser = webdriver.Chrome(ChromeDriverManager().install())

        browser.get(url)
        time.sleep(1)

        elem = browser.find_element_by_tag_name("body")

        no_of_pagedowns =90

        while no_of_pagedowns:
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.65)
            no_of_pagedowns-=1

        texts = browser.find_elements_by_class_name("_eYtD2XCVieq6emjKBH3m")
        dates_post = browser.find_elements_by_class_name("_3jOxDPIQ0KaOWpzvSQo-1s")
        comments_post = browser.find_elements_by_class_name("FHCV02u6Cp2zYL0fhQPsO")

        same = []

        texts = texts[slice(0, len(texts)-8)]


        for index, text in enumerate(texts):
            print(text.text)
            if text.text not in titles:
                titles.append(text.text)
            else:
                same.append(index)

        for index, date in enumerate(dates_post):
            if index not in same:
                if "hours" in date.text or "hour" in date.text or "minute" in date.text or "minutes" in date.text:
                    dates.append(date.text)
                elif index+1 <= len(titles):
                    same.append(index)
                    print(titles[index], date.text)
                    titles.pop(index)


        for index, comment in enumerate(comments_post):
            if index not in same:
                print(comment.text.replace(' comments', '').replace(' comment', ''))
                comments.append(comment.text.replace(' comments', '').replace(' comment', ''))

        print(comments)

        print('length : ', len(titles), len(comments))
        print('length2 : ', len(nbComments), len(getCryptoListCsv.cryptos))


        browser.close()

    newTitles = []

    # sort with date


    # compare crypto name in title
    for index, crypto in enumerate(getCryptoListCsv.cryptos):
        for titleIndex, title in enumerate(titles):
            if crypto.casefold() in title.casefold():
                    stats[index] = stats[index]+1
                    if len(comments) >= titleIndex+1:
                        print('comment', comments[titleIndex])
                        if "k" in comments[titleIndex]:
                            nbComments[index]+=float(comments[titleIndex].replace('k', ''))*1000
                        else:
                            nbComments[index]+=float(comments[titleIndex])
                    else:
                        nbComments[index]+=0
                    for indexWord, negativeWord in enumerate(getNegativeWord.negativeWords):
                        if negativeWord.casefold() in title.casefold():
                                negativeWordCount[index] = negativeWordCount[index]+1
                    for indexWord, positiveWord in enumerate(getPositiveWord.positiveWords):
                        if positiveWord.casefold() in title.casefold():
                                positiveWordCount[index] = positiveWordCount[index]+1



    # moyenne différence positive word et negative word

    medianPositiveWord = []
    median2PositiveWord = 0

    for index, crypto in enumerate(getCryptoListCsv.cryptos):
        if positiveWordCount[index] != 0 and negativeWordCount[index] != 0:
            medianPositiveWord.append(round(float(positiveWordCount[index])/float(negativeWordCount[index]), 2))
        else:
            medianPositiveWord.append(0)

    for median in medianPositiveWord:
        median2PositiveWord+=median

    medianPositiveWordSort = []
    for median in medianPositiveWord:
        if(median != 0):
            medianPositiveWordSort.append(median)

    median2PositiveWord = (median2PositiveWord/len(medianPositiveWordSort))

    def actualDateInt():
        strings = time.strftime("%Y,%m,%d,%H,%M")
        t = strings.split(',')
        a = [int(x) for x in t]
        dateStr = ''
        for nb in a:
            if len(nb) < 2:
                nb = "0"+nb
            dateStr+=str(nb)
        return str(dateStr)
    
    resultData = []

    for index, cours in enumerate(getCryptoListCsv.cours):
        if stats[index] > 5: # get just data with > 5 nb reading
            if float(cours.replace('%', '')) > 0:
                resultData.append(str(getCryptoListCsv.cryptos[index])+", "+str(cours)+", "+str(getCryptoListCsv.price[index])+", "+str(medianPositiveWord[index])+', '+str(stats[index])+', '+str(nbComments[index])+', '+str(positiveWordCount[index])+', '+str(negativeWordCount[index])+', '+str(getCryptoListCsv.rank[index])+', '+actualDateInt()+', positif')
            else:
                resultData.append(str(getCryptoListCsv.cryptos[index])+", "+str(cours)+", "+str(getCryptoListCsv.price[index])+", "+str(medianPositiveWord[index])+', '+str(+stats[index])+', '+str(nbComments[index])+', '+str(positiveWordCount[index])+', '+str(negativeWordCount[index])+', '+str(getCryptoListCsv.rank[index])+', '+actualDateInt()+', negatif')

    headCsvResult = ["crypto", "cours", "moyenne positive word", "nb reading", "positive word count", "negative word count"]


    with open('./data/'+str(datetime.today().strftime("%m-%d-%Y-%H:%M"))+'-'+urlUse+'.csv','w', newline='') as f_output:
        csv_output = csv.writer(f_output, delimiter=",")
        csv_output.writerows([x.split(',') for x in resultData])

    with open('./data/texts_csv/texts-'+str(datetime.today().strftime("%d-%m-%Y-%H:%M"))+'.csv','w', newline='') as f_output:
        csv_output = csv.writer(f_output, delimiter=",")
        csv_output.writerows([x.split(',') for x in titles])

    time.sleep(3000)

