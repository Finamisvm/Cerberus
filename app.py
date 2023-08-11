import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from threading import Thread
from mathstuffs.modelInterface import ModelResult
from mathstuffs.ssodel import SSodel
from entity.account import Account;
from entity.accountType import AccountType
from entity.loginMethod import LoginMethod
from entity.twoFactorMethod import TwoFactorMethod
from entity.recoveryMethod import RecoveryMethod

from flask import Flask, render_template, request, redirect
from uuid import uuid4, UUID
import sqlite3
import db
import networkx as nx


app = Flask(__name__)

db.init_db()

# to do: make accounts linkable, same user-id for multiple inputs!
@app.route("/", methods=["GET"])
def index():
    userID = uuid4()
    return redirect("/" + str(userID))

@app.route("/<userID>")
def userSite(userID: str):
    parsed = UUID(userID)
    return render_template("index.html", userID=userID)

@app.route("/<userID>/account/update", methods = ["POST"])
def create_account(userID: str):
    parsedID = UUID(userID)
    name = request.values.get("accountName")
    type = AccountType(int(request.values.get("accountType")))
    loginMethod = LoginMethod(int(request.values.get("loginMethod")))
    twoFactorMethod = TwoFactorMethod(int(request.values.get("twoFAMethod")))
    recoveryMethod = RecoveryMethod(int(request.values.get("recoveryMethod")))
    account = Account(
        userID=parsedID,
        name=name,  
        type=type, 
        loginMethod=loginMethod, 
        twoFAMethod=twoFactorMethod, 
        fallbackMethod=recoveryMethod,
        )
    db.insert_account(account)
    return render_template("account/edit.html", accountTypes=AccountType, loginMethods=LoginMethod, recoveryMethods=RecoveryMethod, twoFAMethods=TwoFactorMethod, userID=userID)

@app.route("/<userID>/account/edit", methods=["GET"])
def account_edit(userID: str):
    return render_template("account/edit.html", accountTypes=AccountType, loginMethods=LoginMethod, recoveryMethods=RecoveryMethod, twoFAMethods=TwoFactorMethod, userID=userID)
    
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

@app.route("/<userID>/model/calc")
def calc(userID: str):
    accounts = db.get_accounts(userID)
    model = SSodel()
    results = model.calc(accounts)

    
    G = nx.Graph()
    nodes = []
    for result in results:
        nodes.append((result.account.name, {"color": "red"}))
    G.add_nodes_from(nodes)

    nx.draw(G, with_labels=True, )
    plt.savefig("static/" + userID + ".png")
    plt.clf()

        # thread = Thread(target=draw_task, args=(userID, results))
        # thread.start()

    return render_template("modelTable.html", results=results)

def draw_task(userID: str, results: list[ModelResult]):
    G = nx.Graph()
    nodes = []
    for result in results:
        nodes.append((result.account.name, {"color": "red"}))
    G.add_nodes_from(nodes)

    nx.draw(G, with_labels=True, )
    plt.savefig("static/" + userID + ".png")
    plt.clf()