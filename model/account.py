from model.accountType import AccountType
from model.recoveryMethod import RecoveryMethod
from model.twoFactorMethod import TwoFactorMethod
from .loginMethod import LoginMethod
from uuid import uuid4

class Account:
    userID: uuid4 = uuid4()
    name: str = ""
    type: AccountType or None = None # email, social media, ...
    loginMethod: LoginMethod = LoginMethod.PASSWORD
    twoFAEnabled: bool = False
    twoFAMethod: TwoFactorMethod = None
    fallbackMethod: RecoveryMethod = None
    connectedAccounts = [] # list of Accounts

    def __init__(self, 
                 userID = uuid4(), 
                 name = "", 
                 type = None, 
                 loginMethod = LoginMethod.PASSWORD, 
                 twoFAEnabled = False,
                 twoFAMethod = None,
                 fallbackMethod = None,
                 connectedAccounts = []):
        self.userID = userID
        self.name = name
        self.type = type
        self.loginMethod = loginMethod
        self.twoFAEnabled = twoFAEnabled
        self.twoFAMethod = twoFAMethod
        self.fallbackMethod = fallbackMethod
        self.connectedAccounts = connectedAccounts