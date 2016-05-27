from __future__ import division
__author__ = 'agrimasthana'

import mysql.connector
import csv


def setup():
    global dbconfig
    dbconfig = config['config']


def gettotal():
    csr = cnx.cursor()
    csr.execute('Select COUNT(*) from Tweets.Tweets')
    totaltweet = csr.fetchone()
    csr.close()
    return totaltweet[0]


def getpositive():
    csr = cnx.cursor()
    csr.execute("Select COUNT(*) from Tweets.Tweets where sentiment='pos'")
    postweet = csr.fetchone()
    csr.close()
    return postweet[0]


def getnegative():
    csr = cnx.cursor()
    csr.execute("Select COUNT(*) from Tweets.Tweets where sentiment='neg'")
    negtweet = csr.fetchone()
    csr.close()
    return negtweet[0]


def cleandb():
    csr = cnx.cursor()
    csr.execute("delete from Tweets.`Tweets`")
    cnx.commit()
    return -1

if __name__ == '__main__':
    config = {}
    execfile('settings.conf', config)
    setup()
    try:
        cnx = mysql.connector.connect(**dbconfig)
    except Exception as E:
        print E
    tweets = gettotal()
    positive = getpositive()
    negative = getnegative()
    print "Optimism is :", positive / tweets * 100, "%"
    print "Pessimism is :", negative / tweets * 100, "%"
    print "undecided are :", 100 - (positive / tweets * 100 + negative / tweets * 100), "%"
    with open('data.csv', 'w') as csvfile:
        fieldnames = ['age', 'population']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'age': 'Positive', 'population': positive / tweets * 100})
        writer.writerow({'age': 'Negative', 'population': negative / tweets * 100})
        # writer.writerow({'age': 'Neutral', 'population': 100 - (positive / tweets * 100 + negative / tweets * 100)})

    res = cleandb()
    if res == -1:
        print("Done :)")