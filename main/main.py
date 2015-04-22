from tokens.TokenType import TokenType
from tokens.Token import Token
import re

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

def scan_link(file_string, i):
    token_list.append(Token(TokenType.link_begin))
    i += 2
    link_url = ""
    link_section = ""
    link_text = ""
    url_added = False
    while i < len(file_string):
        if file_string[i] == "#":
            token_list.append(Token(TokenType.link_url, link_url))
            url_added = True
            token_list.append(Token(TokenType.link_section_sep))
            i += 1
            while i < len(file_string) and file_string[i] != "|" and file_string[i:i+1] != "]]":
                link_section += file_string[i]
                i += 1
            token_list.append(Token(TokenType.link_section, link_section))
        if file_string[i] == "|":
            if not url_added:
                token_list.append(Token(TokenType.link_url, link_url))
                url_added = True
            token_list.append(Token(TokenType.link_text_sep))
            i += 1
            while i < len(file_string):
                if file_string[i] == "]" and file_string[i+1] == "]":
                    break
                link_text += file_string[i]
                i += 1
            token_list.append(Token(TokenType.link_text, link_text))
        if file_string[i] == "]" and file_string[i+1] == "]":
            if not url_added:
                token_list.append(Token(TokenType.link_url, link_url))
                url_added = True
            token_list.append(Token(TokenType.link_end))
            i += 2
            break
        link_url += file_string[i]
        i += 1
    return i
	
with open('../test.txt', 'r') as file:
    file_string = file.read()
    i = 0
    content = ""
    length = len(file_string)
    while i < length:
        if file_string[i] == "=":
            if (i+1 <= length - 1 and file_string[i + 1] == "="):
                if (i+2 <= length - 1 and file_string[i + 2] == "="):
                    if (i+3 <= (length - 1) and file_string[i + 3] == "="):
                        if (i+4 <= length - 1 and file_string[i + 4] == "="):
                            if (i+5 <= length -1 and file_string[i + 5] == "="):
                                token_list.append(Token(TokenType.content, content))
                                content = ""
                                token_list.append(Token(TokenType.heading_level6))
                                i += 6
                                continue
                            else:
                                token_list.append(Token(TokenType.content, content))
                                content = ""
                                token_list.append(Token(TokenType.heading_level5))
                                i += 5
                                continue
                        else:
                            token_list.append(Token(TokenType.content, content))
                            content = ""
                            token_list.append(Token(TokenType.heading_level4))
                            i += 4
                            continue
                    else:
                        token_list.append(Token(TokenType.content, content))
                        content = ""
                        token_list.append(Token(TokenType.heading_level3))
                        i += 3
                        continue
                else:
                    token_list.append(Token(TokenType.content, content))
                    content = ""
                    token_list.append(Token(TokenType.heading_level2))
                    i += 2
                    continue
            else:
                token_list.append(Token(TokenType.content, content))
                content = ""
                token_list.append(Token(TokenType.heading_level1))
                i += 1
                continue
        elif i+1 <= length - 1 and file_string[i] == "*" and file_string[i+1] == "*":
            token_list.append(Token(TokenType.content, content))
            content = ""
            token_list.append(Token(TokenType.text_bold_symbol))
            i += 2
        elif i+1 <= length - 1 and file_string[i] == "/" and file_string[i+1] == "/":
            token_list.append(Token(TokenType.content, content))
            content = ""
            token_list.append(Token(TokenType.text_italics_symbol))
            i += 2
        elif i+1 <= length - 1 and file_string[i] == "_" and file_string[i+1] == "_":
            token_list.append(Token(TokenType.content, content))
            content = ""
            token_list.append(Token(TokenType.text_underlined_symbol))
            i += 2
        elif i+1 <= length - 1 and file_string[i] == "'" and file_string[i+1] == "'":
            token_list.append(Token(TokenType.content, content))
            content = ""
            token_list.append(Token(TokenType.text_monospaced_symbol))
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
        elif (re.match(r'\n  \s*\*',file_string[i:])):
            it = re.finditer(r'\*',file_string[i:])
            for match in it:
               off = match.start()
               break
            token_list.append(Token(TokenType.list_unord_symbol))
            i += off
            continue
        elif (re.match(r'\n  \s*-',file_string[i:])):
            it = re.finditer(r'-',file_string[i:])
            for match in it:
               off = match.start()
               break
            token_list.append(Token(TokenType.list_ord_symbol))
            i += off
            continue
        elif file_string[i] == "^" or file_string[i] == "|":
            i = scan_table(file_string, i)
        elif file_string[i] == "[" and file_string[i+1] == "[":
            i = scan_link(file_string, i)
        else:
           # print(i)
            #print(file_string[i])
            i += 1
    token_list.append(Token(TokenType.content, content))
    content = ""

print(token_list)