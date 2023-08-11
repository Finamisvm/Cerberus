from entity.accountType import AccountType
from entity.recoveryMethod import RecoveryMethod
from entity.twoFactorMethod import TwoFactorMethod
from entity.loginMethod import LoginMethod
from uuid import uuid4

class Account:
    id: int = 0,
    userID: uuid4 = uuid4()
    name: str = ""
    type: AccountType or None = None # email, social media, ...
    loginMethod: LoginMethod = LoginMethod.PASSWORD
    twoFAEnabled: bool = False
    twoFAMethod: TwoFactorMethod = None
    fallbackMethod: RecoveryMethod = None
    connectedEmail: int = 0
    connectedSSOAccounts = [] # list of Accounts
    connectedFallbackAccounts = [] # list of Accounts

    def __init__(self, 
                 id = 0,
                 userID = uuid4(), 
                 name = "", 
                 type = None, 
                 loginMethod = LoginMethod.PASSWORD, 
                 twoFAEnabled = False,
                 twoFAMethod = None,
                 fallbackMethod = None,
                 connectedEmail = 0,
                 connectedSSOAccounts = [],
                 connectedFallbackAccounts = []):
        self.id = id
        self.userID = userID
        self.name = name
        self.type = type
        self.loginMethod = loginMethod
        self.twoFAEnabled = twoFAEnabled
        self.twoFAMethod = twoFAMethod
        self.fallbackMethod = fallbackMethod
        self.connectedEmail = connectedEmail
        self.connectedSSOAccounts = connectedSSOAccounts
        self.connectedFallbackAccounts = connectedFallbackAccounts
