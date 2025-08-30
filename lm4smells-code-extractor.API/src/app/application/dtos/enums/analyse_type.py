from enum import Enum

class AnalyseType(str, Enum):
    large_class = "large-class"
    long_method = "long-method"
    long_parameter_list = "long-parameter-list"