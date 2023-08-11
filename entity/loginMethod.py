from enum import Enum

class LoginMethod(Enum):
    PASSWORD = 1
    EMAIL = 2
    SMS = 3
    BIOMETRICS = 4
    CERTIFICATE = 5
    TOKEN = 6
    MAGIC_LINK = 7
    SSO = 8
