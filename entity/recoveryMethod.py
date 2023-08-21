from enum import Enum

class RecoveryMethod(Enum):
    NONE = 0
    EMAIL = 1
    SMS = 2
    CODES = 3
    APP = 4
    SECURITY_QUESTIONS = 5
    
