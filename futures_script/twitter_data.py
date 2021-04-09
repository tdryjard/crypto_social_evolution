

# SCRIPT DOSEN'T WORK !!!

from bs4 import BeautifulSoup
import urllib.request
import csv
import getCryptoListCsv
import getCryptoList
import getNegativeWord
import getPositiveWord
from datetime import datetime

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager



# specify the url

urlsB = ['https://twitter.com/zhusu', 'https://twitter.com/woonomic',
'https://twitter.com/JRNYcrypto', 'https://twitter.com/crypto']

urls = ['https://twitter.com/search?q=%23crypto&src=typed_query']

titles = []
dates = []
comments = []
likes = []
stats = [0] * len(getCryptoListCsv.cryptos)
negativeWordCount = [0] * len(getCryptoListCsv.cryptos)
positiveWordCount = [0] * len(getCryptoListCsv.cryptos)
nbComments = [0] * len(getCryptoListCsv.cryptos)
nbLikes = [0] * len(getCryptoListCsv.cryptos)

urlUse = 'urls'

for url in urls:

    browser = webdriver.Chrome(ChromeDriverManager().install())

    browser.get(url)
    time.sleep(1)

    elem = browser.find_element_by_tag_name("body")

    no_of_pagedowns =50

    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.10)
        no_of_pagedowns-=1

    texts = browser.find_elements_by_class_name("_eYtD2XCVieq6emjKBH3m")
    dates_post = browser.find_elements_by_class_name("_3jOxDPIQ0KaOWpzvSQo-1s")
    comments_post = browser.find_elements_by_class_name("FHCV02u6Cp2zYL0fhQPsO")
    like_post = browser.find_elements_by_class_name("FHCV02u6Cp2zYL0fhQPsO")
    hashtag_post = browser.find_elements_by_class_name("FHCV02u6Cp2zYL0fhQPsO")
    posts = browser.find_element_by_xpath('/html/body/div[0]/div[0]/div[0]/main/div/div/div')

    print(posts)
    

    same = []

    print(len(texts), len(dates_post))

    texts = texts[slice(0, len(texts)-8)]


    for index, text in enumerate(posts):
        if text.text and text.text not in titles:
            titles.append(text.text)
        else:
            same.append(index)

    for post in titles:
        print(post)

    for index, date in enumerate(dates_post):
        if index not in same:
            dates.append(date.text)

    for index, comment in enumerate(comments_post):
        if index not in same:
            print(comment.text.replace(' comments', '').replace(' comment', ''))
            comments.append(comment.text.replace(' comments', '').replace(' comment', ''))

    print(comments)

    print('length : ', len(titles), len(comments))
    print('length2 : ', len(nbComments), len(getCryptoListCsv.cryptos))


    browser.close()

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

totalStat = 0

for stat in stats:
    totalStat+=stat

middleStat = totalStat/len(stats)


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
        dateStr+=str(nb)
    return str(dateStr)

# récupération des cryptos avec une moyenne de mots positive au dessus de la moyenne

hightCours = []
hightCrypto = []

resultPrevision = []
resultData = []
resultData_no_percent = []

for index, cours in enumerate(getCryptoListCsv.cours):
    if medianPositiveWord[index] > median2PositiveWord and stats[index] > 5:
        hightCours.append(cours)
        hightCrypto.append(getCryptoListCsv.cryptos[index])
        print("crypto", getCryptoListCsv.cryptos[index], cours, 'price : ', str(getCryptoListCsv.price[index]), "median positive :", medianPositiveWord[index], 'nb read :', stats[index], 'positive word :', positiveWordCount[index], 'negative word :', negativeWordCount[index], 'nb comments : ', nbComments[index] )
        resultPrevision.append(str(getCryptoListCsv.cryptos[index])+", "+str(cours)+", "+str(getCryptoListCsv.price[index])+", "+str(medianPositiveWord[index])+', '+str(stats[index])+str(nbComments[index])+', '+str(positiveWordCount[index])+', '+str(negativeWordCount[index]))
    if stats[index] > 5:
        if float(cours.replace('%', '')) > 0:
            resultData.append(str(getCryptoListCsv.cryptos[index])+", "+str(cours)+", "+str(getCryptoListCsv.price[index])+", "+str(medianPositiveWord[index])+', '+str(stats[index])+', '+str(nbComments[index])+', '+str(positiveWordCount[index])+', '+str(negativeWordCount[index])+', '+str(getCryptoListCsv.rank[index])+', '+actualDateInt()+', positif')
            resultData_no_percent.append(str(getCryptoListCsv.cryptos[index])+", "+str(medianPositiveWord[index])+', '+str(stats[index])+', '+str(nbComments[index])+', '+str(positiveWordCount[index])+', '+str(negativeWordCount[index])+', '+str(getCryptoListCsv.rank[index])+', '+actualDateInt()+', positif')
        else:
            resultData.append(str(getCryptoListCsv.cryptos[index])+", "+str(cours)+", "+str(getCryptoListCsv.price[index])+", "+str(medianPositiveWord[index])+', '+str(+stats[index])+', '+str(nbComments[index])+', '+str(positiveWordCount[index])+', '+str(negativeWordCount[index])+', '+str(getCryptoListCsv.rank[index])+', '+actualDateInt()+', negatif')
            resultData_no_percent.append(str(getCryptoListCsv.cryptos[index])+", "+str(medianPositiveWord[index])+', '+str(stats[index])+', '+str(nbComments[index])+', '+str(positiveWordCount[index])+', '+str(negativeWordCount[index])+', '+str(getCryptoListCsv.rank[index])+', '+actualDateInt()+', negatif')


totalHightCours = 0.0

for cours in hightCours:
    totalHightCours+=float(cours.replace('%', ''))

print('median positive word :', median2PositiveWord)
print('total pourcentage cryptos selectionnées', totalHightCours)

resultPrevision.append('median positive word : '+str(median2PositiveWord))
resultPrevision.append('total pourcentage cryptos selectionnées : '+str(totalHightCours))

headCsvResult = ["crypto", "cours", "moyenne positive word", "nb reading", "positive word count", "negative word count"]

with open('./default-previsions/data-'+str(datetime.today().strftime("%d-%m-%Y-%H:%M"))+'.csv','w', newline='') as f_output:
    csv_output = csv.writer(f_output, delimiter=",")
    csv_output.writerows([headCsvResult])
    csv_output.writerows([x.split(',') for x in resultPrevision])

with open('./data/data-'+str(datetime.today().strftime("%d-%m-%Y-%H:%M"))+'-'+urlUse+'.csv','w', newline='') as f_output:
    csv_output = csv.writer(f_output, delimiter=",")
    csv_output.writerows([x.split(',') for x in resultData])

with open('./data/texts_csv/texts-'+str(datetime.today().strftime("%d-%m-%Y-%H:%M"))+'.csv','w', newline='') as f_output:
    csv_output = csv.writer(f_output, delimiter=",")
    csv_output.writerows([x.split(',') for x in titles])



time.sleep(216000)