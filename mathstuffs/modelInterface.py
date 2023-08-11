from entity.account import Account

class ModelResult:
    account: Account = None
    value: float = 0.0

    def __init__(self, account, value):
        self.account = account
        self.value = value

class ModelInterface:
    def calc(accounts: list[Account]) -> list[ModelResult]:
        pass
