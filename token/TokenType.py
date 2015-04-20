from enum import Enum


class TokenType(Enum):
    whitespace = 1
    text_bold_symbol = 2
    text_underlined_symbol = 3
    text_monospaced_symbol = 4
    text_del_begin = 5
    text_del_end = 6
    text_sub_begin = 7
    text_sub_end = 8
    text_sup_begin = 9
    text_sup_end = 10
    text_code_begin = 11
    text_code_end = 12
    heading_level1 = 13
    heading_level2 = 14
    heading_level3 = 15
    heading_level4 = 16
    heading_level5 = 17
    heading_level6 = 18