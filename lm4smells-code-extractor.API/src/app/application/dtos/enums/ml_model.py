from enum import Enum

class MLModel(str, Enum):
    LGBM = "LGBM"   #long method and Large Class
    KNN = "KNN"     #long method and long parameter list and long class
    LDA = "LDA"     #long method and long class
    RIDGE = "RIDGE" #long method and Large Class
    SGD = "SGD"     #long method and long parameter list
    GAUSSIAN = "GAUSSIAN" #long parameter list
    QDA = "QDA"     #long parameter list
    IR = "IR"       #large class

