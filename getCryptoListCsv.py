import csv

cryptos = []
cours = []
rank = []
price = []

with open('./csv/crypto-list.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=' ')
    line_count = 0
    for row in csv_reader:
        for word in row:
            rank.append(word.split(',')[0].casefold())
            cryptos.append(word.split(',')[1].casefold())
            cours.append(word.split(',')[2].casefold())
            price.append(word.split(',')[3].casefold())

