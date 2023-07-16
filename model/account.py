from loginMethod import LoginMethod
from uuid import uuid4

class Account:
    userId = None
    name = ""
    type = None # email, social media, ...
    loginMethod = LoginMethod.PASSWORD
    twoFAEnabled = False
    twoFAMethod = None
    fallbackMethod = None
    connectedAccounts = [] # list of Accounts

    def __init__(self, userId = uuid4()):
        self.userId = userId