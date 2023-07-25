from mathstuffs.ssodel import SSodel
from model.account import Account;
from model.accountType import AccountType
from model.loginMethod import LoginMethod
from model.twoFactorMethod import TwoFactorMethod
from model.recoveryMethod import RecoveryMethod

from flask import Flask, render_template, request
import sqlite3
import db

app = Flask(__name__)

db.init_db()

# to do: make accounts linkable, same user-id for multiple inputs!

@app.route("/account/update", methods = ["POST"])
def create_account():
    name = request.values.get("accountName")
    type = AccountType(int(request.values.get("accountType")))
    loginMethod = LoginMethod(int(request.values.get("loginMethod")))
    twoFactorMethod = TwoFactorMethod(int(request.values.get("twoFAMethod")))
    recoveryMethod = RecoveryMethod(int(request.values.get("recoveryMethod")))
    account = Account(
        name=name, 
        type=type, 
        loginMethod=loginMethod, 
        twoFAMethod=twoFactorMethod, 
        fallbackMethod=recoveryMethod,
        )
    db.insert_account(account)
    return render_template("account/edit.html", accountTypes=AccountType, loginMethods=LoginMethod, recoveryMethods=RecoveryMethod)

@app.route("/", methods=["GET"])
def hello_world():
    return render_template("index.html")

@app.route("/account/edit", methods=["GET"])
def account_edit():
    return render_template("account/edit.html", accountTypes=AccountType, loginMethods=LoginMethod, recoveryMethods=RecoveryMethod)

@app.route("/account/2fa", methods=["GET"])
def account_twoFAFrom():    
    is2FAActive = request.values.get('twoFAActive')
    if is2FAActive is None:
        return ""
    
    return render_template("account/twoFAAuthentication.html", twoFAMethods=TwoFactorMethod)
    
@app.route("/account/otheraccs", methods=["GET"])
def account_otherAccsFrom():    
    otherAccs = request.values.get('otherAccs')
    if otherAccs is None:
        return ""
   
@app.route("/api/account", methods=["GET", "POST"])
def account():
    accType = request.form.get('accType')
    otherAccs = request.form.get('otherAccs')
    loginMethod = request.form.get('loginMethod')
    backupMethod = request.form.get('recoveryMethod')

    conn = sqlite3.connect('UserData_db.sqlite')
    c = conn.cursor()
    insintab = "INSERT INTO accounts_table (accType, otherAccs, loginMethod, recoveryMethod) values (?, ?, ?, ?)"
    c.execute(insintab, (accType, otherAccs, loginMethod, backupMethod))
    conn.commit()
    conn.close()

    return render_template("index.html", accType=accType, otherAccs=otherAccs, loginMethod=loginMethod, backupMethod=backupMethod)

@app.route("/result")
def result():
    return "result of accounts"

@app.route("/model/calc")
def calc():
    accounts = db.get_accounts()
    model = SSodel()
    results = model.calc(accounts)
    for r in results:
        print("acc: " + r.account.name + " | value: " + str(r.value))
    return ""