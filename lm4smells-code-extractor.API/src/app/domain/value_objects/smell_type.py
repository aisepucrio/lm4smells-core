from enum import Enum

class SmellType(Enum):
    LONG_METHOD = "Long Method"
    NO_LONG_METHOD = "No Long Method"
    LONG_PARAMETER_LIST = "Long Parameter List"
    NO_LONG_PARAMETER_LIST = "No Long Parameter List"
    LARGE_CLASS = "Large Class"
    NO_LARGE_CLASS = "No Large Class"
    DATA_CLASS = "Data Class"
    NO_DATA_CLASS = "No Data Class"
    LAZY_CLASS = "Lazy Class"
    NO_LAZY_CLASS = "No Lazy Class"
    MAGIC_NUMBERS = "Magic Numbers"
    NO_MAGIC_NUMBERS = "No Magic Numbers"