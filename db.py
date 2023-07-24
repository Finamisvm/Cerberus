import sqlite3

from model.account import Account
from model.accountType import AccountType
from model.loginMethod import LoginMethod
from model.twoFactorMethod import TwoFactorMethod

def init_db():
    connection = sqlite3.connect("UserData.db")
    c = connection.cursor()
    c.execute("""
              CREATE TABLE IF NOT EXISTS accounts_table (
                userId VARCHAR(100), 
                accName VARCAHR, 
                accType VARCHAR, 
                loginMethod VARCHAR, 
                twoFactorMethod VARCHAR, 
                recoveryMethod VARCHAR, 
                otherAccsConnected BOOL)
              """)
    connection.commit()
    connection.close()

def get_accounts():
    connection = sqlite3.connect("UserData.db")
    cur = connection.cursor()
    sql = "SELECT * FROM accounts_table"
    cur.execute(sql)
    rows = cur.fetchall()

    accounts = []
    for row in rows:
        accounts.append(Account(
            userId=row[0],
            name=row[1],
            accountType=AccountType[row[2]],
            loginMethod=LoginMethod[row[3]],
            twoFAMethod=TwoFactorMethod[row[4]],
            fallbackMethod=row[5],
            connectedAccounts=[],
        ))

    connection.close()
    return accounts



def insert_account(account: Account):
    connection = sqlite3.connect("UserData.db")
    cursor = connection.cursor()
    sql = """
        INSERT INTO accounts_table 
        (userId, accName, accType, loginMethod, twoFactorMethod, recoveryMethod) 
        values (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(sql, (
        str(account.userId),
        account.name, 
        account.type.name, 
        account.loginMethod.name, 
        account.twoFAMethod.name, 
        account.fallbackMethod.name,
        ))
    connection.commit()
    connection.close()

    
