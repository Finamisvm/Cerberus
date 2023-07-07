import numpy as np;
import pandas as pd;
import seaborn as sns;
import seaborn.objects as so;

from flask import Flask, render_template, request
import sqlite3

conn = sqlite3.connect('UserData_db.sqlite')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS userData (accName VARCHAR, accType VARCHAR)')
conn.commit()
conn.close()

app = Flask(__name__)

datatable = []

@app.route("/", methods=["GET"])
def hello_world():
    return render_template("index.html")

@app.route("/api/account", methods=["GET", "POST"])
def account():
    accName = request.form.get('accName')
    accType = request.form.get('accType')
    otherAccs = request.form.get('otherAccs')
    loginMethod = request.form.get('loginMethod')
    backupMethod = request.form.get('backupMethod')

    conn = sqlite3.connect('UserData_db.sqlite')
    c = conn.cursor()
    insintab = "INSERT INTO userData (accName, accType) values (?, ?)"
    c.execute(insintab, (accName, accType))
    conn.commit()
    conn.close()

    return render_template("index.html", accName=accName, accType=accType, otherAccs=otherAccs, loginMethod=loginMethod, backupMethod=backupMethod)

@app.route("/result")
def result():
    return "result of accounts"

#seems to kill laptop: print(request.values.get(AccName))

def writeDatainTable(userinput):
    # for i = 1, nofuckingideahowmuch:
    #     datatable[i] = userinput
    
    # return datatable
    pass

def printDatatable(datatable):
    pass


