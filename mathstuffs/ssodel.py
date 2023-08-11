from mathstuffs.modelInterface import ModelInterface, ModelResult
from entity.account import Account
from entity.loginMethod import LoginMethod


class SSodel(ModelInterface):
    def calc(self, accounts: list[Account]) -> list[ModelResult]:
        result = []
        for acc in accounts:
            result.append(ModelResult(
                account=acc, 
                value=self.calc_login_method(acc.loginMethod)
                )
            )
        return result

    def calc_login_method(self, login_method: LoginMethod) -> float:
        if login_method == LoginMethod.PASSWORD:
            return 1.0
        elif login_method == LoginMethod.SMS:
            return 2.0
        elif login_method == LoginMethod.CERTIFICATE:
            return 6.0
        elif login_method == LoginMethod.BIOMETRICS:
            return 4.0
        elif login_method == LoginMethod.EMAIL:
            return 4.0
        elif login_method == LoginMethod.MAGIC_LINK:
            return 3.0
        elif login_method == LoginMethod.SSO:
            return 5.0
        elif login_method == LoginMethod.TOKEN:
            return 3.0