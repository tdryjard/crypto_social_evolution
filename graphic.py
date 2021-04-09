import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
from datetime import datetime

min_diff_time = -2 # minimum d'heure entre les deux données comparées enregistré dans la data
max_diff_time = -4
diff_with_last_date_to_median = 50 # 100 = 1 hour / maximum d'heures de différence avec les autres données pour calculer une moyenne ou injecter en tant que nouvelle donnée
max_diff_time_to_median = 0.1 # maximum de différence entre les différences de temps de comparaison pour calculer une moyenne
min_diff_time_to_median = -0.1
min_diff_to_new_value = 200  # 100 = 1 hour / maximum d'heures de différence avec les autres données pour injecter en tant que nouvelle donnée
min_date = 202104031601 # date minimun pour le graphic

"""
EXEMPLE :

min_diff_time = -2
max_diff_time = -4
diff_with_last_date_to_median = 50
max_diff_time_to_median = 0.1
min_diff_time_to_median = -0.1
min_date = 202104011601

min_diff_time : les données que l'on va retenir ont été comparées avec des données au minimum plus ancienne de 2h

max_diff_time : les données que l'on va retenir ont été comparées avec des données au maximum plus ancienne de 4h

diff_with_last_date_to_median
max_diff_time_to_median
min_diff_time_to_median : toutes les données qui ont moins de 50 minutes décart et qui ont une comparaison de moins de 10 minutes d'écarts sont misent ensemble pour faire une moyenne

min_date : sont retenu que les données après le 01-04-2021 à 16h01

"""
# SELECT FILE

data = './data/social-evolution/evolution-09-04-2021-16:10.csv'

names = ['crypto', 'prix', 'prix avant', 'difference prix', 'nb read', 'good word', 'bad word', 'comments', 'date', 'difference temps']
dataset = []

with open(data) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=' ')
    line_count = 0
    for row in csv_reader:
        for word in row:
            realRow = []
            for index in word.split(','):
                realRow.append(index.casefold())
        dataset.append(realRow)

dataset = list(dataset)
groups = []

same = []


for index1, data1 in enumerate(dataset):
    group = []
    if data1[0] not in same and float(data1[9]) < 0:
        same.append(data1[0])
        for index2, data2 in enumerate(dataset):
            if len(data2) > 9 and data2[0] == data1[0] and float(data2[9]) < min_diff_time and float(data2[9]) > max_diff_time:
                group.append(data2)
    if(len(group) > 1):
        groups.append(group)

evolutions = []




for groupNotSort in groups:
    group = sorted(list(groupNotSort), key=lambda x: -float(list(x)[8]))
    same = []
    for index, crypto in enumerate(group):
        totalEvolution = 0
        totalPrice = 0
        totalBadWord = 0
        totalGoodWord = 0
        nbEvolution = 0
        if index not in same and int(crypto[8]) > min_date:
            for index2, crypto2 in enumerate(group):
                if int(crypto[8]) - int(crypto2[8]) < diff_with_last_date_to_median and (int(crypto[9]) - int(crypto2[9]) < max_diff_time_to_median or int(crypto[9]) - int(crypto2[9]) > min_diff_time_to_median):
                    totalEvolution+=float(crypto2[4])
                    totalPrice+=float(crypto2[3])
                    totalBadWord+=float(crypto2[6])
                    totalGoodWord+=float(crypto2[5])
                    nbEvolution+=1
                    same.append(index2)
            
            if crypto[0] == "bnb":
                print(index, ': ', 'crypto 1 date : ', crypto[8], 'crypto 2 date : ', crypto2[8],'crypto 1 diff : ', crypto[9], 'crypto 2 diff : ', crypto2[9])
            if (len(evolutions) < 1 or (evolutions[len(evolutions) - 1][0] == crypto[0] and (int(evolutions[len(evolutions) - 1][1]) - int(crypto[8]) > min_diff_to_new_value))) or evolutions[len(evolutions) - 1][0] != crypto[0]:
                evolutions.append([crypto[0], crypto[8], round((totalEvolution/nbEvolution), 2), round((totalPrice/nbEvolution), 2), round((totalBadWord/nbEvolution), 2), round((totalGoodWord/nbEvolution), 2)])


groups2 = []

same = []

for index1, crypto in enumerate(evolutions):
    group = []
    if crypto[0] not in same:
        same.append(crypto[0])
        for index2, crypto2 in enumerate(evolutions):
            if crypto[0] == crypto2[0] and crypto2 not in group:
                group.append(crypto2)
        groups2.append(group)


print(len(groups2))


def convertTime(time):
    time = list(time)
    year = time[0]+time[1]+time[2]+time[3]
    month = time[4]+time[5]
    day = time[6]+time[7]
    hour = str(time[8]+time[9])
    minutes = str(time[10]+time[11])
    a = day+'/'+month+'/'
    b = hour+':'+minutes
    return(str(a+b))

csvData = []

for group in groups2:
    data = sorted(list(group), key=lambda x: float(list(x)[1]))
    data = np.array(data)

    csvData.append(data)

with open('./data/graphic-data/'+str(datetime.today().strftime("%d-%m-%Y-%H:%M"))+'.csv','w', newline='') as f_output:
        csv_output = csv.writer(f_output,delimiter=',')
        csv_output.writerows(csvData)



for group in groups2:
    data = sorted(list(group), key=lambda x: float(list(x)[1]))
    data = np.array(data)

    for index, crypto in enumerate(data):
        data[index][1] = convertTime(crypto[1])


    # x axis values
    x = data[:,1]
    # corresponding y axis values
    y = data[:,2].astype(float)
    y2 = data[:,3].astype(float)
    y3 = data[:,4].astype(float)
    y4 = data[:,5].astype(float)
    
    # plotting the points 
    
    # evolution number of reading crypto
    plt.plot(x, y, color='blue', linewidth = 2,
            marker='o', markerfacecolor='black', markersize=8)

    # evolution of crypto price
    plt.plot(x, y2, color='yellow', linewidth = 2,
            marker='o', markerfacecolor='black', markersize=8)

    # evolution of negatif word count
    plt.plot(x, y3, color='red', linewidth = 2,
            marker='o', markerfacecolor='black', markersize=8)

    # evolution of positif word count
    plt.plot(x, y4, color='green', linewidth = 2,
            marker='o', markerfacecolor='black', markersize=8)
    
    # setting x and y axis range
    plt.ylim(-80,80)
    plt.xlim(0, 8)
    
    # naming the x axis
    plt.xlabel('date')
    # naming the y axis
    plt.ylabel('evolution')
    
    # giving a title to my graph
    plt.title(group[0][0])

    plt.grid()
    
    # function to show the plot
    plt.show()