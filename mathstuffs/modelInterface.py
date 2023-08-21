from entity.account import Account

class SecurityScoreResult:
    account: Account = None
    secScore: float = 0.0
    actualSecScore: float = 0.0
    secScoreConnectedAccounts: list = []

    def __init__(self, account, secScore):
        self.account = account
        self.secScore = secScore
        self.actualSecScore = secScore
        self.secScoreConnectedAccounts = []
        self.hints = []

class SecurityEngine:
    def calc(accounts: list[Account]) -> list[SecurityScoreResult]:
        pass
