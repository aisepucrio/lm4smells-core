from enum import Enum

class Approach(str, Enum):
    LM = "lm"
    AST = "ast"
    ML = "ml"
    DL = "dl"