# crypto_social_evolution
cryptocurrency price prediction experiment by analyzing the evolution of discussions on social networks


# 1) library install and go in project environment

cmd : pip install -r requirements.txt

cmd : source ./env/bin/activate

# 2) generate data with scraping reddit (file : reddit_data.py)

## cmd :  python reddit_data.py

This script open a browser (default browser safari, you can change this line 56), the script scroll and get all titles in cryptos groups.

## The data is save in data folder, details of data file generate :

a axemple of line in data file :

btc, -3.77%, 56018.59, 1.97, 26, 144.0, 61, 31, 1, 202104091249, negatif

details :

[crypto, current cours, current price, ratio negatif/positif word, number of times crypto appears in headlines, number of comments in post with cryptos (btc in exemple), number of positifs words in titles with crypto, number of negatif words in titles with crypto, current rank, current date, negatif/positif label with cours]

# 3) data traitment to compare and get social evolution (file : evolutionSocial.py)

cmd : python evolutionSocial.py

## This script processes the data to render a csv file in ./data/social-evolution, details of data file generate :

a axemple of line in data file :

btc,56018.59,57862.23,-3.19,-44.0,-61.0,-50.0,547.0,202104072213,-28

details :

[crypto, current price, crypto price in the previous data compared, number of times crypto appears in headlines, number of positifs words in titles with crypto, number of negatif words in titles with crypto, number of comments in post with cryptos, current date, time interval between the previous compared data and this data]

# 4) data traitment to generate graphic and data for machine learning (file : graphic.py)

cmd : python graphic.py

This script processes the data to compact them into groups of cryptos in date order and on average with the data close in time.

## Graphic legend :

Yellow : evolution of crypto price

Blue : evolution of reading crypto count

Green : evolution of positif word count

Red : evolution of negatif word count

## CSV file save in ./data/graphic-data , details of data file generate :

a axemple of line in data file :

['game' '202104062349' '-5.2' '-0.79' '-15.4' '-8.8'],['game' '202104071901' '-7.67' '-1.38' '-14.0' '-1.67'],['game' '202104072213' '8.5' '-2.07' '0.0' '13.0'],['game' '202104082145' '17.0' '0.0' '0.0' '26.0']

details :
[crypto, date of data, evolution reading count, price evolution, bad word evolution, good word evolution]

# 5) machine learning with graphic data (file : machineLearning.py)

cmd : python machineLearning.py

Experiment machine learning with precesses data in ./data/graphic-data

Render predictions in ./data/predictions
