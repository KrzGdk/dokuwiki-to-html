from tokens.TokenType import TokenType


class Token:
    def __init__(self, token_type):
        self.token_type = token_type

    def __str__(self):
        if self.token_type == TokenType.heading_level1:
            return "="
        elif self.token_type == TokenType.heading_level2:
            return "=="
        elif self.token_type == TokenType.heading_level3:
            return "==="
        elif self.token_type == TokenType.heading_level4:
            return "===="
        elif self.token_type == TokenType.heading_level5:
            return "====="
        elif self.token_type == TokenType.heading_level6:
            return "======="
        elif self.token_type == TokenType.text_bold_symbol:
            return "**"
        elif self.token_type == TokenType.text_italics_symbol:
            return "//"
        elif self.token_type == TokenType.text_underlined_symbol:
            return "__"
        else:
            return "dupa"

    __repr__ = __str__