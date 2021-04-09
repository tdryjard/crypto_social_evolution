import csv

positiveWords = []

with open('./csv/positive-word.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        for word in row:
            positiveWords.append(word.replace(' ', '').casefold())