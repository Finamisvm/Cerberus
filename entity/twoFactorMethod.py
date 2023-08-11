from enum import Enum

class TwoFactorMethod(Enum):
    NONE = 0
    AUTHENTICATOR = 1
    SECURITY_QUESTION = 2
    SMS = 3
    EMAIL = 4
    HARDWARE_TOKEN = 5
    
