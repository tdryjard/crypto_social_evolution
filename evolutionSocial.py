# Load libraries
import pandas as pd
import csv
from datetime import datetime,  timedelta
import numpy as np
from pandas.plotting import scatter_matrix
import getCryptoListCsv
from arch.unitroot import KPSS
import getCryptoListCsv
import glob
import os
import xlsxwriter as xlsw
from pandas import ExcelWriter

from pandas.plotting import scatter_matrix
from matplotlib import pyplot

import time


# Load dataset
datas = glob.glob("./data/*.csv")

results = []
lastPrice = []

resCryptos = []

labels = []

datas.sort(key=os.path.getmtime, reverse=True)


print(datas)

same = []

i = 1
while i < len(datas):
    for iData, data in enumerate(datas):
        if iData+i < len(datas):
            names = ["crypto", "cours", "price", "moyenne positive word", "nb reading", "nb comments", "positive word count", "negative word count", "rank", "date", "type"]
            dataset1 = pd.read_csv(data, names=names)
            dataset2 = pd.read_csv(datas[iData+i], names=names)


            dataset1 = dataset1.values
            dataset2 = dataset2.values


            for index, crypto in enumerate(dataset1):
                dataset1[index][1] = float(crypto[1].replace('%', ''))
                dataset1[index][10] = crypto[10].replace(' ', '')

            for index, crypto in enumerate(dataset2):
                dataset2[index][1] = float(crypto[1].replace('%', ''))
                dataset2[index][10] = crypto[10].replace(' ', '')

            def translateDate(date):
                dateSplit = list(str(date))
                newDate = ''
                if len(dateSplit) < 12:
                    b = dateSplit[:]
                    b.insert(4, 0)
                    dateSplit = b
                for index, nb in enumerate(dateSplit):
                    if index > 3:
                        if index%2 == 0:
                            newDate+=','
                    newDate+=str(nb)
                return newDate

            def diff_dates(date1, date2):

                    difference = [0, 0, 0, 0, 0]
                    for index, nb in enumerate(str(date1).split(',')):
                        difference[index] = int(str(date2).split(',')[index]) - int(nb)
                    
                    hoursDiff = 0
                    for index, diff in enumerate(difference):
                        if index == 0 and diff != 0:
                            hoursDiff+= diff*(365*24)
                        if index == 1 and diff != 0:
                            hoursDiff+= diff*(30*24)
                        if index == 2 and diff != 0:
                            hoursDiff+= diff*24
                        if index == 3 and diff != 0:
                            hoursDiff+= diff
                        if index == 4 and diff != 0:
                            if diff > 50:
                                hoursDiff+=1
                                
                    print('date1 : ', date1, 'date2 : ', date2, 'hours diff : ', hoursDiff, 'diffrence : ', difference)

                    return int(hoursDiff)

            # round number

            def myround(x, base=5):
                return base * round(float(x) / base)

            # add result in data

            resultCompare = []

            resultReturn = []

            for index, crypto1 in enumerate(dataset1):
                for index2, crypto2 in enumerate(dataset2):
                    if crypto1[0] == crypto2[0]:
                            difference_date = diff_dates(translateDate(crypto1[9]), translateDate(crypto2[9]))
                            difference_price = round(((crypto1[2]-crypto2[2])/crypto2[2]*100), 2)
                            difference_read = ((crypto1[4]-crypto2[4])/crypto2[4]*100)
                            difference_comments = 0
                            difference_good_word = 0
                            difference_bad_word = 0
                            try :
                                    difference_comments = ((crypto1[5]-crypto2[5])/crypto2[5]*100)
                            except:
                                print('0')
                            try :
                                difference_good_word = ((crypto1[6]-crypto2[6])/crypto2[6]*100)
                            except:
                                print('0')
                            try :
                                difference_bad_word = ((crypto1[7]-crypto2[7])/crypto2[7]*100)
                            except:
                                print('0')
                            resultCompare.append(crypto1[0]+' '+'price : '+str(crypto1[2])+' '+' read evolution : '+
                            str(round(difference_read, 0))+'% in '+str(difference_date)+
                            'h the '+str(translateDate(crypto1[9]))
                            +' commments evolution : '+str(round(difference_comments, 0))+'%'
                            +' positif word : '+str(round(difference_good_word, 0))+'%'
                            +' negatif word : '+str(round(difference_bad_word, 0))+'%')
                            results.append(crypto1[0]+','+str(crypto1[2])+','+str(crypto2[2])+','+str(difference_price)+','+str(round(difference_read, 0))+','+str(round(difference_good_word, 0))+','+str(round(difference_bad_word, 0))+','+str(round(difference_comments, 0))+','+str(crypto1[9])+','+str(difference_date))
                            lastPrice.append(crypto2[2])
                            if difference_price > 0:
                                labels.append('up')
                            else:
                                labels.append('down')
    i+=1
                                

resEvolution = []

for crypto in getCryptoListCsv.cryptos:
    cryptoRes = []
    for res in results:
        if res.split(',')[0] == crypto:
            cryptoRes.append(res)
    resEvolution.append(reversed(cryptoRes))

newResults = []

for res in results:
    stock = []
    resSplit = res.split(',')
    for split in resSplit:
        stock.append(split)
    newResults.append(stock)


newResults = np.array(newResults)

data = newResults[:,1:10]
cryptos = newResults[:,0]

data = pd.DataFrame(data,
                index = cryptos,
                columns = ['prix', 'prix avant', 'difference prix', 'date', 'difference temps', 'nb read', 'good word', 'bad word', 'comments'])



writer = ExcelWriter('PythonExport.xlsx')
data.to_excel(writer,'Sheet5')
writer.save()


with open('./data/social-evolution/evolution-'+str(datetime.today().strftime("%d-%m-%Y-%H:%M"))+'.csv','w', newline='') as f_output:
            csv_output = csv.writer(f_output, delimiter=",")
            csv_output.writerows([x for x in list(newResults)])