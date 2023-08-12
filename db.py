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
    c.execute("""
                CREATE TABLE IF NOT EXISTS login_connections (
                    userID VARCHAR(100),
                    account_id INTEGER,
                    login_account_id INTEGER
                )
              """)
    c.execute("""
                CREATE TABLE IF NOT EXISTS recovery_connections (
                    userID VARCHAR(100),
                    account_id INTEGER,
                    recovery_account_id INTEGER
                )
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

def get_connections(userID: str) -> list[(int, int)]:
    connection = sqlite3.connect("UserData.db")
    cur = connection.cursor()
    result = []
    sql = "SELECT account_id, login_account_id FROM login_connections WHERE userID=?;"
    cur.execute(sql, (userID,))
    rows = cur.fetchall()
    for row in rows:
        result.append((row[0], row[1]))
        
    sql = "SELECT account_id, recovery_account_id FROM recovery_connections WHERE userID=?;"
    cur.execute(sql, (userID,))
    rows = cur.fetchall()
    for row in rows:
        result.append((row[0], row[1]))
    return result


def insert_account(account: Account) -> int:
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
    id = cursor.lastrowid
    connection.commit()
    connection.close()
    return id

def insert_recovery_connection(userID: UUID, accountID: int, recoveryAccountID: int):
    connection = sqlite3.connect("UserData.db")
    cursor = connection.cursor()
    sql = """
        INSERT INTO recovery_connections 
            (userID, account_id, recovery_account_id) 
            VALUES (?, ?, ?)
    """
    cursor.execute(sql, (str(userID), accountID, recoveryAccountID))
    connection.commit()
    connection.close()

    
def insert_login_connection(userID: UUID, accountID: int, loginAccountID: int):
    connection = sqlite3.connect("UserData.db")
    cursor = connection.cursor()
    sql = """
        INSERT INTO login_connections 
            (userID, account_id, login_account_id) 
            VALUES (?, ?, ?)
    """
    cursor.execute(sql, (str(userID), accountID, loginAccountID))
    connection.commit()
    connection.close()
