from entity.twoFactorMethod import TwoFactorMethod
from mathstuffs.modelInterface import SecurityEngine, SecurityScoreResult
from entity.account import Account
from entity.loginMethod import LoginMethod


class SSodel(SecurityEngine):
    accountDict = {}

    def __init__(self) -> None:
        super().__init__()
        self.accountDict = {}

    def calc(self, accounts: list[Account]) -> list[SecurityScoreResult]:
        results = []
        for acc in accounts:
            secScore = self.calc_sec_score_for_account(acc, accounts)
            result = SecurityScoreResult(acc, secScore)

            self.calc_connected_accounts(result, accounts, acc.connectedLoginAccounts)
            self.calc_connected_accounts(result, accounts, acc.connectedRecoveryAccounts)
                
            results.append(result)
        return results

    def calc_connected_accounts(self, result: SecurityScoreResult, accounts: list[Account], connectedAccounts: list[int]):
        for loginAccountId in connectedAccounts:
                loginAccount = self.get_account(accounts, loginAccountId)
                secScoreLoginAcc = self.calc_sec_score_for_account(loginAccount, accounts)
                result.secScoreConnectedAccounts.append([loginAccountId, secScoreLoginAcc])
                if secScoreLoginAcc < result.actualSecScore:
                    result.actualSecScore = secScoreLoginAcc
                

    def get_account(self, accounts: list[Account], id: int) -> Account:
        for acc in accounts:
            if acc.id == id:
                return acc


    def calc_sec_score_for_account(self, account: Account, accounts: list[Account]) -> float:
        if self.accountDict.get(account.id) != None:
            return self.accountDict.get(account.id)
        
        loginMethod = account.loginMethod
        secScore = 0.0
        if loginMethod == LoginMethod.PASSWORD:
            secScore = 3.0
        elif loginMethod == LoginMethod.SMS:
            secScore = 4.0
        elif loginMethod == LoginMethod.CERTIFICATE:
            secScore = 8.0
        elif loginMethod == LoginMethod.BIOMETRICS:
            secScore = 7.0
        elif loginMethod == LoginMethod.TOKEN:
            secScore = 7.0
        elif loginMethod == LoginMethod.MAGIC_LINK or loginMethod == LoginMethod.SSO or loginMethod == LoginMethod.EMAIL:
            for acc in account.connectedLoginAccounts:
                connectedAccScore = self.calc_sec_score_for_account(self.get_account(accounts, acc), accounts)
                if secScore == 0.0:
                    secScore = connectedAccScore
                elif connectedAccScore < secScore:
                    secScore = connectedAccScore

        if account.twoFAMethod != TwoFactorMethod.NONE:
            secScore = secScore + 2

        min = secScore
        for acc in account.connectedRecoveryAccounts:
            connectedAccScore = self.calc_sec_score_for_account(self.get_account(accounts, acc), accounts)
            if connectedAccScore < min:
                min = connectedAccScore

        secScore = secScore - ((secScore - min) / 2)

        self.accountDict[account.id] = secScore
        return secScore