# Load libraries
import pandas as pd
import csv
from datetime import datetime,  timedelta
import numpy as np
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.calibration import CalibratedClassifierCV
import getCryptoListCsv
from arch.unitroot import KPSS
import getCryptoListCsv
import glob
import os

import time

data = './data/graphic-data/09-04-2021-16:13.csv'

names = ['crypto', 'date', 'evolution read', 'evolution price', 'good word ev', 'bad word ev', 'label']

dataset = []

with open(data) as csv_file:
    csv_reader = list(csv.reader(csv_file, delimiter=','))
    line_count = 0
    for row in csv_reader:
        realRow = []
        for array in row:
            array = array.replace('[', '').replace(']', '').replace('"', "").replace("'", "")
            print(array)
            print(type(array.split(',')))
            realRow.append(array.split(' '))
        dataset.append(realRow)
        

dataset = list(dataset)


for index, data in enumerate(dataset):
    for index2, crypto in enumerate(data):
        if len(data) > index2+1:
            if data[index2+1][3] > crypto[3]:
                dataset[index][index2].append('up')
            else:
                dataset[index][index2].append('down')
        else:
            dataset[index][index2].append('none')
            
    


newDataset = []

for data in dataset:
    for crypto in data:
        newDataset.append(crypto)
        


predictions = []
cryptosPredictions = []

for index, data in enumerate(newDataset):
    if data[6] == "none":
        predictions.append(data)
        cryptosPredictions.append(newDataset[index][0])
        newDataset.pop(index)
        

for index, data in enumerate(newDataset):
    if data[6] == "none":
        newDataset.pop(index)
        
predictions = np.array(predictions)

newDataset = np.array(newDataset)

newDataset = pd.DataFrame(newDataset[:,0:7], columns = names)
newDataset.crypto = pd.Categorical(pd.factorize(newDataset.crypto)[0])
newDataset = np.array(newDataset)


# Split-out validation dataset
data = newDataset[:,1:6].astype(float)
label = newDataset[:,6]
data_train, data_validation, label_train, label_validation = train_test_split(data, label, test_size=0.15, random_state=10000)

# Spot Check Algorithms
models = []
models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC(gamma='auto')))
# evaluate each model in turn
results = []
names = []

for name, model in models:
    kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
    cv_results = cross_val_score(model, data_train, label_train, cv=kfold, scoring='accuracy')
    results.append(cv_results)
    names.append(name)
    print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))

    # Make predictions on validation dataset

for name, model in models:
    model.fit(data_train, label_train)

    predictionsResult = model.predict(predictions[:,1:6])


    printResult = []

    
    for index, predict in enumerate(predictionsResult):
        printResult.append(str(cryptosPredictions[index])+','+predictionsResult[index]+','+str(predictions[:,1:6][index]))

    
    with open('./data/predictions/prediction-'+str(datetime.today().strftime("%d-%m-%Y-%H:%M"))+'-'+name+'-with-cours'+str(index)+'.csv','w', newline='') as f_output:
        csv_output = csv.writer(f_output, delimiter=",")
        csv_output.writerows([x.split(',') for x in printResult])
    
