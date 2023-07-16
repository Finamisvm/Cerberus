import numpy as np;
import pandas as pd;
import seaborn as sns;
import seaborn.objects as so;
from model.accountType import AccountType
from model.loginMethod import LoginMethod
from model.twoFactorMethod import TwoFactorMethod

from flask import Flask, render_template, request
import sqlite3

conn = sqlite3.connect('UserData_db.sqlite')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS accounts_table (accName VARCHAR, accType VARCHAR, otherAccs VARCHAR, loginMethod VARCHAR, backupMethod Varchar)')
conn.commit()
conn.close()

app = Flask(__name__)

datatable = []

@app.route("/", methods=["GET"])
def hello_world():
    return render_template("index.html")


@app.route("/account/edit", methods=["GET"])
def account_edit():
    return render_template("account/edit.html", accountTypes=AccountType, loginMethods=LoginMethod)

@app.route("/account/2fa", methods=["GET"])
def account_twoFAFrom():    
    is2FAActive = request.values.get('twoFAActive')
    if is2FAActive is None:
        return ""
    
    return render_template("account/towFAAutentication.html", twoFAMethods=TwoFactorMethod)
    


@app.route("/api/account", methods=["GET", "POST"])
def account():
    accName = request.form.get('accName')
    accType = request.form.get('accType')
    otherAccs = request.form.get('otherAccs')
    loginMethod = request.form.get('loginMethod')
    backupMethod = request.form.get('backupMethod')

    conn = sqlite3.connect('UserData_db.sqlite')
    c = conn.cursor()
    insintab = "INSERT INTO accounts_table (accName, accType, otherAccs, loginMethod, backupMethod) values (?, ?, ?, ?, ?)"
    c.execute(insintab, (accName, accType, otherAccs, loginMethod, backupMethod))
    conn.commit()
    conn.close()

    return render_template("index.html", accName=accName, accType=accType, otherAccs=otherAccs, loginMethod=loginMethod, backupMethod=backupMethod)

@app.route("/result")
def result():
    return "result of accounts"