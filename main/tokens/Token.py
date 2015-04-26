from tokens.TokenType import TokenType


class Token:
    def __init__(self, token, content=""):
        
        self.token = token
        self.content = content

    def __repr__(self):
        t = self.token
        if t == TokenType.heading_level1:
            t = "heading_level1"
        elif t == TokenType.heading_level2:
            t = "heading_level2"
        elif t == TokenType.heading_level3:
            t = "heading_level3"
        elif t == TokenType.heading_level4:
            t = "heading_level4"
        elif t == TokenType.heading_level5:
            t = "heading_level5"
        elif t == TokenType.heading_level6:
            t = "heading_level6"
        elif t == TokenType.text_bold_symbol:
            t = "text_bold"
        elif t == TokenType.text_italics_symbol:
            t = "text_italic"
        elif t == TokenType.text_underlined_symbol:
            t = "text_underlined"
        elif t == TokenType.text_del_begin:
            t = "del_begin"
        elif t == TokenType.text_del_end:
            t = "del_end"
        elif t == TokenType.text_code_begin:
            t = "code_begin"
        elif t == TokenType.text_code_end:
            t = "code_end"
        elif t == TokenType.text_sup_begin:
            t = "sup_begin"
        elif t == TokenType.text_sup_end:
            t = "sup_end"
        elif t == TokenType.text_sub_begin:
            t = "sub_begin"
        elif t == TokenType.text_sub_end:
            t = "sub_end"
        elif t == TokenType.list_unord_symbol:
            t = "list_unord"
        elif t == TokenType.list_ord_symbol:
            t = "list_ord"
        elif t == TokenType.cell_merge_symbol:
            t = "cell_merge"
        elif t == TokenType.tab_heading_sep:
            t = "tab_heading"
        elif t == TokenType.pipe_symbol:
            t = "pipe_symbol"
        elif t == TokenType.two_spaces:
            t = "two_spaces"
        elif t == TokenType.new_line:
            t = "new_line"
        elif self.token == TokenType.content:
            t = self.content
        elif self.token == TokenType.link_begin:
            t = "link_begin"
        elif self.token == TokenType.link_section_sep:
            t = "link_section_sep"
        elif self.token == TokenType.link_text_sep:
            t = "link_text_sep"
        elif self.token == TokenType.footnote_begin:
            t = "footnote_begin"
        elif self.token == TokenType.footnote_end:
            t = "footnote_end"
        elif self.token == TokenType.image_begin:
            t = "image_begin"
        elif self.token == TokenType.image_end:
            t = "image_end"
        elif self.token == TokenType.link_end:
            t = "link_end"
        else:
            t = "other"

        return t