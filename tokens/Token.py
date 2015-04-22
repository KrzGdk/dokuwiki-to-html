from tokens.TokenType import TokenType


class Token:
    def __init__(self, token_type, content=""):
        self.token_type = token_type
        self.content = content

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
        elif self.token_type == TokenType.text_monospaced_symbol:
            return "''"
        elif self.token_type == TokenType.cell_merge_symbol:
            return ":::"
        elif self.token_type == TokenType.tab_heading_sep:
            return "^"
        elif self.token_type == TokenType.tab_normal_sep:
            return "|"
        elif self.token_type == TokenType.tab_left_margin or self.token_type == TokenType.tab_right_margin:
            return "  "
        elif self.token_type == TokenType.tab_row_end:
            return "ROW_SEP(NEWLINE)"
        elif self.token_type == TokenType.content:
            return self.content
        elif self.token_type == TokenType.link_text:
            return self.content
        elif self.token_type == TokenType.link_section:
            return self.content
        elif self.token_type == TokenType.link_url:
            return self.content
        elif self.token_type == TokenType.link_begin:
            return "[["
        elif self.token_type == TokenType.link_section_sep:
            return "#"
        elif self.token_type == TokenType.link_text_sep:
            return "|"
        elif self.token_type == TokenType.link_end:
            return "]]"
        else:
            return "inne"

    __repr__ = __str__