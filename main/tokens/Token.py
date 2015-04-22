from tokens.TokenType import TokenType

class Token:
    def __init__(self, token, content=""):
        
        self.token = token
        self.content = content

    def __repr__(self):
        print(self.token)
        t = self.token
        if(t == TokenType.heading_level1): t = "heading_level1"
        elif(t == TokenType.heading_level2): t = "heading_level2"
        elif(t == TokenType.heading_level3): t = "heading_level3"
        elif(t == TokenType.heading_level4): t = "heading_level4"
        elif(t == TokenType.heading_level5): t = "heading_level5"
        elif(t == TokenType.heading_level6): t = "heading_level6"
        elif(t == TokenType.text_bold_symbol): t = "bold"
        elif(t == TokenType.text_italics_symbol): t = "italic"
        elif(t == TokenType.text_underlined_symbol): t = "undelined"
        elif(t == TokenType.text_del_begin) : t = "del_begin"
        elif(t == TokenType.text_del_end) : t = "del_end"
        elif(t == TokenType.text_code_begin) : t = "code_begin"
        elif(t == TokenType.text_code_end) : t = "code_end"
        elif(t == TokenType.text_sup_begin) : t = "sup_begin"
        elif(t == TokenType.text_sup_end) : t = "sup_end"
        elif(t == TokenType.text_sub_begin) : t = "sub_begin"
        elif(t == TokenType.text_sub_end) : t = "sub_end"
        elif(t == TokenType.list_unord_symbol) : t = "list_unord"
        elif(t == TokenType.list_ord_symbol) : t = "list_ord"
        elif(t == TokenType.cell_merge_symbol): t = ":::"
        elif(t == TokenType.tab_heading_sep): t = "^"
        elif(t == TokenType.tab_normal_sep): t = "|"
        elif(t == TokenType.tab_left_margin or t == TokenType.tab_right_margin): t = "  "
        elif(t == TokenType.tab_row_end): t = "ROW_SEP(NEWLINE)"
        elif self.token == TokenType.content: t = self.content
        elif self.token == TokenType.link_text: t = self.content 
        elif self.token == TokenType.link_section: t = self.content
        elif self.token == TokenType.link_url: t = self.content
        elif self.token == TokenType.link_begin: t = "[["
        elif self.token == TokenType.link_section_sep: t = "#"
        elif self.token == TokenType.link_text_sep: t = "|"
        elif self.token == TokenType.link_end: t = "]]"
        else: t = "inne"

        return ( t )