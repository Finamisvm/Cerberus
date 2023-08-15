import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from mathstuffs.modelInterface import ModelResult
from mathstuffs.ssodel import SSodel
from entity.account import Account
from entity.accountType import AccountType
from entity.loginMethod import LoginMethod
from entity.twoFactorMethod import TwoFactorMethod
from entity.recoveryMethod import RecoveryMethod

from flask import Flask, render_template, request, redirect
from uuid import uuid4, UUID
import db
import networkx as nx


app = Flask(__name__)

db.init_db()

PREFIX_LOGIN_SELECTION="selectLogin"
PREFIX_RECOVERY_SELECTION="selectRecovery"

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
    connectedEmail = 0
    isEmailConnected = request.values.get("emailConnected")
    if isEmailConnected != None:
        connectedEmail = int(request.values.get("connectedEmail"))
    account = Account(
        userID=parsedID,
        name=name,  
        type=type, 
        loginMethod=loginMethod, 
        twoFAMethod=twoFactorMethod, 
        fallbackMethod=recoveryMethod,
        connectedEmail=connectedEmail
        )
    accountId = db.insert_account(account)
    # check for login accounts
    for key in request.form.keys():
        if key.startswith(PREFIX_LOGIN_SELECTION):
            db.insert_login_connection(parsedID, accountId, request.form.get(key))

    # check for recovery accounts
    for key in request.form.keys():
        if key.startswith(PREFIX_RECOVERY_SELECTION):
            db.insert_recovery_connection(parsedID, accountId, request.form.get(key))

    return render_template("account/edit.html", accountTypes=AccountType, loginMethods=LoginMethod, recoveryMethods=RecoveryMethod, twoFAMethods=TwoFactorMethod, userID=userID)

@app.route("/<userID>/account/select/email")
def select_email_account(userID: str):
    accounts = db.get_accounts(userID)

    isEmailConnected =  request.values.get("emailConnected")
    if isEmailConnected == None:
        return ""
    return render_template("account/selection.html", accounts=accounts, fieldName="connectedEmail")

@app.route("/<userID>/account/select/login")
def select_sso_account(userID: str):
    accounts = db.get_accounts(userID)

    loginMethod =  LoginMethod(int(request.values.get("loginMethod")))
    if loginMethod == LoginMethod.SSO:
        return render_template("account/multiSelect.html", accounts=accounts, prefix=PREFIX_LOGIN_SELECTION)
    return ""

@app.route("/<userID>/account/select/recovery")
def select_recovery_account(userID: str):
    accounts = db.get_accounts(userID)

    recoveryMethod =  RecoveryMethod(int(request.values.get("recoveryMethod")))
    if recoveryMethod == RecoveryMethod.EMAIL or recoveryMethod == RecoveryMethod.OTHER_ACCOUNT:
        return render_template("account/multiSelect.html", accounts=accounts, prefix=PREFIX_RECOVERY_SELECTION)
    return ""

@app.route("/<userID>/account/edit", methods=["GET"])
def account_edit(userID: str):
    return render_template("account/edit.html", accountTypes=AccountType, loginMethods=LoginMethod, recoveryMethods=RecoveryMethod, twoFAMethods=TwoFactorMethod, userID=userID)
    
@app.route("/account/otheraccs", methods=["GET"])
def account_otherAccsFrom():    
    otherAccs = request.values.get('otherAccs')
    if otherAccs is None:
        return ""
   
@app.route("/result")
def result():
    return "result of accounts"

@app.route("/<userID>/model/calc")
def calc(userID: str):
    accounts = db.get_accounts(userID)
    con = db.get_connections(userID)
    model = SSodel()
    results = model.calc(accounts)

    
    G = nx.Graph()
    nodes = []
    edges = []
    for result in results:
        nodes.append((result.account.id, {"color": "red"}))
        if result.account.connectedEmail != 0:
            edges.append((result.account.id, result.account.connectedEmail))
    
    edges = edges + con
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    nx.draw(G, with_labels=True, )
    plt.savefig("static/" + userID + ".png")
    plt.clf()

    return render_template("modelTable.html", results=results)