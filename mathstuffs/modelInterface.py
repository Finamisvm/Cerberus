from entity.account import Account

class ModelResult:
    account: Account = None
    secScore: float = 0.0
    hints: list[str] = []

    def __init__(self, account, secScore):
        self.account = account
        self.secScore = secScore
        self.hints = []

class ModelInterface:
    def calc(accounts: list[Account]) -> list[ModelResult]:
        pass
