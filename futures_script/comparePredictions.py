
# SCRIPT DOSEN'T WORK !!!

import csv
import getCryptoList
import getCryptoListCsv
from datetime import datetime
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import numpy as np
import glob

csvFiles = ['./data/predictions/prediction-30-03-2021-17:25-KNN-with-cours.csv', './data/predictions/prediction-30-03-2021-17:25-CART-with-cours.csv']

sameResult = []

stockResults = []

for csvPath in csvFiles:

    cryptos = []
    prices = []
    predictions = []

    results = []

    with open(csvPath) as csv_file:
        csv_reader = list(csv.reader(csv_file, delimiter=','))
        line_count = 0
        for index, row in enumerate(csv_reader):
            for index2, word in enumerate(row):
                print(word.split(','))
                if index2 == 0:
                    cryptos.append(word.casefold())
                if index2 == 1 and 'up' not in word and 'down' not in word:
                    prices.append(word.casefold())
                if index2 == 2:
                    predictions.append(word.casefold())

    print('cryptos', len(cryptos))
    print('prices', len(prices))
    print('predictions', len(predictions))

    def myround(x, base=5):
        return base * round(float(x) / base)

    resultPrediction = []

    ratioPrediction = 0
    resultPercent = 0

    nbCryptoBuy = 0

    for prediction in predictions:
        print(prediction.split(' '))
        if prediction != "down" and int(prediction.split(' ')[3].replace('+', '').replace('%', '')) > 5:
            nbCryptoBuy+=1

    print('nb cryptos buy', nbCryptoBuy)

    for index, cryptoCsv in enumerate(getCryptoListCsv.cryptos):
        for index2, crypto in enumerate(cryptos):
            if cryptoCsv == crypto:
                diffPrice = myround((float(getCryptoListCsv.price[index]) - float(prices[index2]))/float(prices[index2])*100)

                if predictions[index2] != "down" and int(predictions[index2].split(' ')[3].replace('+', '').replace('%', '')) > 5:
                    if round(((float(getCryptoListCsv.price[index]) - float(prices[index2]))/float(prices[index2])*100), 2) > 0:
                        ratioPrediction+=1
                    resultPercent+= round(((float(getCryptoListCsv.price[index]) - float(prices[index2]))/float(prices[index2])*100), 2)
                    print('crypto : ', crypto, 'price : ', prices[index2])
                    print('diff', round(((float(getCryptoListCsv.price[index]) - float(prices[index2]))/float(prices[index2])*100), 2))
                    print('predict', predictions[index2].split(' ')[3].replace('+', '').replace('%', ''))
                    results.append('crypto : '+crypto+' price : '+str(prices[index2])+' predict +'+predictions[index2].split(' ')[3].replace('+', '').replace('%', '')+'%')
                else:
                    if round(((float(getCryptoListCsv.price[index]) - float(prices[index2]))/float(prices[index2])*100), 2) < 0:
                        ratioPrediction+=1
                    print('crypto : ', crypto, 'baad')
                    print('diff', round(((float(getCryptoListCsv.price[index]) - float(prices[index2]))/float(prices[index2])*100), 2))
                    # print('predict', predictions[index2].split(' ')[3].replace('+', '').replace('%', ''))


    ratioPrediction = ratioPrediction/len(cryptos)

    if nbCryptoBuy != 0:
        resultPercent = resultPercent/nbCryptoBuy



    print('ratio'+' : '+str(ratioPrediction))
    print('percent'+' : '+str(resultPercent))
    stockResults.append(results)

sameResult = []

for result1 in stockResults[0]:
    for result2 in stockResults[1]:
        if result1 == result2:
            sameResult.append(result1)

for res in sameResult:
    print(res)

sameResult = np.array(sameResult)

with open('./data/result-predictions/predict-'+str(datetime.today().strftime("%d-%m-%Y-%H:%M"))+'.csv','w', newline='') as f_output:
    csv_output = csv.writer(f_output, delimiter=",")
    csv_output.writerows([x for x in sameResult])