from tokens.TokenType import TokenType
from tokens.Token import Token

token_list = []

with open('../test.txt', 'r') as file:
    file_string = file.read()
    i = 0
    length = len(file_string)
    while i < length:
        if file_string[i] == "=":
            if (i+1 < length - 1 and file_string[i + 1] == "="):
                if (i+2 < length - 1 and file_string[i + 2] == "="):
                    if (i+3 < (length - 1) and file_string[i + 3] == "="):
                        if (i+4 < length - 1 and file_string[i + 4] == "="):
                            if (i+5 < length -1 and file_string[i + 5] == "="):
                                token_list.append(Token(TokenType.heading_level6))
                                i += 6
                                continue
                            else:
                                token_list.append(Token(TokenType.heading_level5))
                                i += 5
                                continue
                        else:
                            token_list.append(Token(TokenType.heading_level4))
                            i += 4
                            continue
                    else:
                        token_list.append(Token(TokenType.heading_level3))
                        i += 3
                        continue
                else:
                    token_list.append(Token(TokenType.heading_level2))
                    i += 2
                    continue
            else:
                token_list.append(Token(TokenType.heading_level1))
                i += 1
                continue
        elif file_string[i] == "*" and file_string[i+1] == "*":
            token_list.append(Token(TokenType.text_bold_symbol))
            i += 2
        elif file_string[i] == "/" and file_string[i+1] == "/":
            token_list.append(Token(TokenType.text_italics_symbol))
            i += 2
        elif file_string[i] == "_" and file_string[i+1] == "_":
            token_list.append(Token(TokenType.text_underlined_symbol))
            i += 2
        elif file_string[i] == "<":		
            if (file_string[i+1:i+5] == "del>"):
               token_list.append(Token(TokenType.text_del_begin))
               i += 4
            elif (file_string[i+1:i+6] == "/del>"):
               token_list.append(Token(TokenType.text_del_end))
               i += 5
            elif (file_string[i+1:i+6] == "code>"):
               token_list.append(Token(TokenType.text_code_begin))
               i += 5
            elif (file_string[i+1:i+7] == "/code>"):
               token_list.append(Token(TokenType.text_code_end))
               i += 6
            elif (file_string[i+1:i+5] == "sup>"):
               token_list.append(Token(TokenType.text_sup_begin))
               i += 4
            elif (file_string[i+1:i+6] == "/sup>"):
               token_list.append(Token(TokenType.text_sup_end))
               i += 5
            elif (file_string[i+1:i+5] == "sub>"):
               token_list.append(Token(TokenType.text_sub_begin))
               i += 4
            elif (file_string[i+1:i+6] == "/sub>"):
               token_list.append(Token(TokenType.text_sub_end))
               i += 5
            i += 1
            continue
        else:
            print(i)
            print(file_string[i])
            i += 1

print(token_list)