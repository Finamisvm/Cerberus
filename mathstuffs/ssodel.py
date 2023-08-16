from mathstuffs.modelInterface import ModelInterface, ModelResult
from entity.account import Account
from entity.loginMethod import LoginMethod


class SSodel(ModelInterface):
    def calc(self, accounts: list[Account]) -> list[ModelResult]:
        results = []
        for acc in accounts:
            secScore = self.calc_sec_score_for_account(acc)
            result = ModelResult(acc, secScore)

            self.calc_connected_accounts(result, accounts, acc.connectedLoginAccounts)
            self.calc_connected_accounts(result, accounts, acc.connectedRecoveryAccounts)
                
            results.append(result)
        return results

    def calc_connected_accounts(self, result: ModelResult, accounts: list[Account], connectedAccounts: list[int]):
        for loginAccountId in connectedAccounts:
                loginAccount = self.get_account(accounts, loginAccountId)
                secScoreLoginAcc = self.calc_sec_score_for_account(loginAccount)

                if secScoreLoginAcc < result.secScore:
                    result.hints.append(
                        "Warning: The security score of your connected account '{name}' is lower than the security score of this account."
                        .format(name=loginAccount.name)
                    )
                

    def get_account(self, accounts: list[Account], id: int) -> Account:
        for acc in accounts:
            if acc.id == id:
                return acc


    def calc_sec_score_for_account(self, account: Account) -> float:
        loginMethod = account.loginMethod
        if loginMethod == LoginMethod.PASSWORD:
            return 1.0
        elif loginMethod == LoginMethod.SMS:
            return 2.0
        elif loginMethod == LoginMethod.CERTIFICATE:
            return 6.0
        elif loginMethod == LoginMethod.BIOMETRICS:
            return 4.0
        elif loginMethod == LoginMethod.EMAIL:
            return 4.0
        elif loginMethod == LoginMethod.MAGIC_LINK:
            return 3.0
        elif loginMethod == LoginMethod.SSO:
            return 5.0
        elif loginMethod == LoginMethod.TOKEN:
            return 3.0