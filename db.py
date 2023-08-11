import sqlite3

from entity.account import Account
from entity.accountType import AccountType
from entity.loginMethod import LoginMethod
from entity.twoFactorMethod import TwoFactorMethod
from uuid import UUID

def init_db():
    connection = sqlite3.connect("UserData.db")
    c = connection.cursor()
    c.execute("""
              CREATE TABLE IF NOT EXISTS accounts_table ( 
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userID VARCHAR(100),
                accName VARCAHR, 
                accType VARCHAR, 
                loginMethod VARCHAR, 
                twoFactorMethod VARCHAR, 
                recoveryMethod VARCHAR,
                emailAccount INTEGER)
              """)
    connection.commit()
    connection.close()

def get_accounts(userID: str) -> list[Account]:
    connection = sqlite3.connect("UserData.db")
    cur = connection.cursor()
    sql = "SELECT * FROM accounts_table WHERE userID=?;"
    cur.execute(sql, (userID,))
    rows = cur.fetchall()

    accounts = []
    for row in rows:
        accounts.append(Account(
            id=int(row[0]),
            userID=UUID(row[1]),
            name=row[2],
            type=AccountType[row[3]],
            loginMethod=LoginMethod[row[4]],
            twoFAMethod=TwoFactorMethod[row[5]],
            fallbackMethod=row[6],
            connectedEmail=row[7],
        ))

    connection.close()
    return accounts



def insert_account(account: Account):
    connection = sqlite3.connect("UserData.db")
    cursor = connection.cursor()
    sql = """
        INSERT INTO accounts_table 
        (userID, accName, accType, loginMethod, twoFactorMethod, recoveryMethod, emailAccount) 
        values (?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(sql, (
        str(account.userID),
        account.name, 
        account.type.name, 
        account.loginMethod.name, 
        account.twoFAMethod.name, 
        account.fallbackMethod.name,
        account.connectedEmail
        ))
    connection.commit()
    connection.close()

    
