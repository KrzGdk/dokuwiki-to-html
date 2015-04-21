from tokens.TokenType import TokenType
from tokens.Token import Token

token_list = []

with open('../test.txt', 'r') as file:
    file_string = file.read()
    i = 0
    while i < len(file_string):
        if file_string[i] == "=":
            if file_string[i + 1] == "=":
                if file_string[i + 2] == "=":
                    if file_string[i + 3] == "=":
                        if file_string[i + 4] == "=":
                            if file_string[i + 5] == "=":
                                token_list.append(Token(TokenType.heading_level6))
                                i += 6
                                continue
                            else:
                                token_list.append(Token(TokenType.heading_level5))
                                i += 5
                                continue
                        else:
                            token_list.append(Token(TokenType.TokenType.heading_level4))
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
        else:
            print(file_string[i])
            i += 1

print(token_list)