from tokens.TokenType import TokenType
from tokens.Token import Token


def scan_cell(file_string, i):
    cell_content = ""
    while True:
        if file_string[i] == " " and file_string[i+1] == " " and file_string[i+2] == "|":
            token_list.append(Token(TokenType.tab_right_margin))
            token_list.append(Token(TokenType.tab_normal_sep))
            added_tokens = 2
            i += 3
            break
        elif file_string[i] == " " and file_string[i+1] == " " and file_string[i+2] == "^":
            token_list.append(Token(TokenType.tab_right_margin))
            token_list.append(Token(TokenType.tab_heading_sep))
            added_tokens = 2
            i += 3
            break
        elif file_string[i] == "|" or file_string[i] == "^":
            if file_string[i] == "|":
                token_list.append(Token(TokenType.tab_normal_sep))
                added_tokens = 1
                i += 1
            elif file_string[i] == "^":
                token_list.append(Token(TokenType.tab_heading_sep))
                added_tokens = 1
                i += 1
            if i < len(file_string) and file_string[i] == " " and file_string[i+1] == " ":
                token_list.append(Token(TokenType.tab_left_margin))
                added_tokens += 1
                i += 2
            break
        else:
            cell_content += file_string[i]
            i += 1
    if cell_content.strip() == ":::":
        token_list.insert(-added_tokens, Token(TokenType.cell_merge_symbol))
    else:
        token_list.insert(-added_tokens, cell_content)
    return i


def scan_row(file_string, i):
    if file_string[i] == "^":
        token_list.append(Token(TokenType.tab_heading_sep))
        i += 1
    elif file_string[i] == "|":
        token_list.append(Token(TokenType.tab_normal_sep))
        i += 1
    if file_string[i] == " " and file_string[i+1] == " ":
        token_list.append(Token(TokenType.tab_left_margin))
        i += 2
    i = scan_cell(file_string, i)
    while i < len(file_string) and file_string[i] != "\n":
        a = file_string[i]
        i = scan_cell(file_string, i)
    else:
        token_list.append(Token(TokenType.tab_row_end))
        i += 1

    return i


def scan_table(file_string, i):
    while i < len(file_string) and (file_string[i] == "^" or file_string[i] == "|"):
        i = scan_row(file_string, i)
    return i

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
        elif file_string[i] == "^" or file_string[i] == "|":
            i = scan_table(file_string, i)
        else:
            print(file_string[i])
            i += 1


print(token_list)