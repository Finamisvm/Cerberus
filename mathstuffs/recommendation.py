from enum import Enum
from entity.account import Account
from entity.loginMethod import LoginMethod
from mathstuffs.modelInterface import ModelResult

class RecommendationSeverity(Enum):
    HINT = 1
    WARNING = 2
    CRITICAL = 3


class Recommendation:
    type: RecommendationSeverity
    text: str
    solution: str

    def __init__(self, type: RecommendationSeverity, text: str, solution: str):
        self.type = type
        self.text = text
        self.solution = solution

class RecommendationResult:
    account: Account = None
    recommendations: list[Recommendation] = []

    def __init__(self, account: Account, recommendations: list[Recommendation]) -> None:
        self.account = account
        self.recommendations = recommendations

class RecommendationEngine:
    def generate_recommendations(self, modelResults: list[ModelResult]) -> dict:
        pass


class SampleRecommendationEngine(RecommendationEngine):
    def generate_recommendations(self, accounts: list[Account], modelResults: list[ModelResult]) -> dict:
        recommendationResults = []
        for result in modelResults:
            recommendationResult = RecommendationResult(
                result.account, []
            )
            recommendationResult.recommendations = recommendationResult.recommendations + self.check_for_sec_level(result, accounts)
            recommendationResult.recommendations = recommendationResult.recommendations + self.check_for_recovery(result, accounts)

            recommendationResults.append(recommendationResult)

        return recommendationResults    

    def check_for_sec_level(self, result: ModelResult, accounts: list[Account]):
        recommendations = []
        if result.secScore < 3:
            recommendations.append(Recommendation(
                type=RecommendationSeverity.CRITICAL,
                text="The used login method is unsecure",
                solution="Change to a more secure login method, e.g. certificate, biometrics, hardware token, magic link",
            ))
        elif result.secScore < 7:
            recommendations.append(Recommendation(
                type=RecommendationSeverity.WARNING,
                text="The used login method is conidered insecure",
                solution="Change to a more secure login method, e.g. certificate, biometrics, hardware token, magic link",
            ))

        for connAccScores in result.secScoreConnectedAccounts:
            connAcc = self.get_account(accounts, connAccScores[0])
            if connAccScores[1] < 3:
                recommendations.append(Recommendation(
                    type=RecommendationSeverity.CRITICAL,
                    text="The connected account '{name}' is insecure".format(name=connAcc.name),
                    solution="Disconnect the account or improve it's security according to the hints for that account",
                ))
            elif connAccScores[1] < 7:
                recommendations.append(Recommendation(
                    type=RecommendationSeverity.WARNING,
                    text="The connected account '{name}' is considered insecure".format(name=connAcc.name),
                    solution="Disconnect the account or improve it's security according to the hints for that account",
                )) 

        return recommendations  

    def check_for_recovery(self, result: ModelResult, accounts: list[Account]):
        acc = result.account
        recommendations = []
        if len(acc.fallbackMethod) == 0:
            recommendations.append(Recommendation(
                account=acc,
                type=RecommendationSeverity.CRITICAL,
                text="Account does not have a recovery method",
                solution="Add a recovery method if possible",
            ))

        return recommendations

    def get_account(self, accounts: list[Account], id: int) -> Account:
        for acc in accounts:
            if acc.id == id:
                return acc
