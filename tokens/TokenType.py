from enum import Enum


class AutoNumber(Enum):
    def __new__(cls):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj


class TokenType(AutoNumber):
    whitespace = ()
    new_line = ()
    text_bold_symbol = ()
    text_italics_symbol = ()
    text_underlined_symbol = ()
    text_monospaced_symbol = ()
    text_del_begin = ()
    text_del_end = ()
    text_sub_begin = ()
    text_sub_end = ()
    text_sup_begin = ()
    text_sup_end = ()
    text_code_begin = ()
    text_code_end = ()
    heading_level1 = ()
    heading_level2 = ()
    heading_level3 = ()
    heading_level4 = ()
    heading_level5 = ()
    heading_level6 = ()