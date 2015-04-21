from tokens.TokenType import TokenType

class Token:
    def __init__(self, token):
        
        self.token = token

    def __repr__(self):
        print(self.token)
        t = self.token
        if(t == TokenType.heading_level3): t = "heading_level3"
        elif(t == TokenType.text_del_begin) : t = "del_begin"
        elif(t == TokenType.text_del_end) : t = "del_end"
        elif(t == TokenType.text_code_begin) : t = "code_begin"
        elif(t == TokenType.text_code_end) : t = "code_end"
        elif(t == TokenType.text_sup_begin) : t = "sup_begin"
        elif(t == TokenType.text_sup_end) : t = "sup_end"
        elif(t == TokenType.text_sub_begin) : t = "sub_begin"
        elif(t == TokenType.text_sub_end) : t = "sub_end"
		
        return ( t )