import re

from dokuwiki_to_html.main.tokens.TokenType import TokenType
from dokuwiki_to_html.main.tokens.Token import Token


class Scanner:
    def scan(self, file_path):
        token_list = []

        with open(file_path, 'r') as file:
            file_string = file.read()
            i = 0
            content = ""
            length = len(file_string)
            while i < length:
                if i + 1 <= length - 1 and file_string[i] == "\\":
                    content += file_string[i + 1]
                    i += 2
                if file_string[i] == "=":
                    if i + 1 <= length - 1 and file_string[i + 1] == "=":
                        if i + 2 <= length - 1 and file_string[i + 2] == "=":
                            if i + 3 <= (length - 1) and file_string[i + 3] == "=":
                                if i + 4 <= length - 1 and file_string[i + 4] == "=":
                                    if i + 5 <= length - 1 and file_string[i + 5] == "=":
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
                elif i + 1 <= length - 1 and file_string[i] == "*" and file_string[i + 1] == "*":
                    token_list.append(Token(TokenType.content, content))
                    content = ""
                    token_list.append(Token(TokenType.text_bold_symbol))
                    i += 2
                elif i + 1 <= length - 1 and file_string[i] == "/" and file_string[i + 1] == "/":
                    token_list.append(Token(TokenType.content, content))
                    content = ""
                    token_list.append(Token(TokenType.text_italics_symbol))
                    i += 2
                elif i + 1 <= length - 1 and file_string[i] == "_" and file_string[i + 1] == "_":
                    token_list.append(Token(TokenType.content, content))
                    content = ""
                    token_list.append(Token(TokenType.text_underlined_symbol))
                    i += 2
                elif i + 1 <= length - 1 and file_string[i] == "'" and file_string[i + 1] == "'":
                    token_list.append(Token(TokenType.content, content))
                    content = ""
                    token_list.append(Token(TokenType.text_monospaced_symbol))
                    i += 2
                elif i + 1 <= length - 1 and file_string[i] == "(" and file_string[i + 1] == "(":
                    token_list.append(Token(TokenType.content, content))
                    content = ""
                    token_list.append(Token(TokenType.footnote_begin))
                    i += 2
                elif i + 1 <= length - 1 and file_string[i] == ")" and file_string[i + 1] == ")":
                    token_list.append(Token(TokenType.content, content))
                    content = ""
                    token_list.append(Token(TokenType.footnote_end))
                    i += 2
                elif i + 1 <= length - 1 and file_string[i] == "{" and file_string[i + 1] == "{":
                    token_list.append(Token(TokenType.content, content))
                    content = ""
                    token_list.append(Token(TokenType.image_begin))
                    i += 2
                elif i + 1 <= length - 1 and file_string[i] == "}" and file_string[i + 1] == "}":
                    token_list.append(Token(TokenType.content, content))
                    content = ""
                    token_list.append(Token(TokenType.image_end))
                    i += 2
                elif file_string[i] == "<":
                    if file_string[i + 1:i + 5] == "del>":
                        token_list.append(Token(TokenType.content, content))
                        content = ""
                        token_list.append(Token(TokenType.text_del_begin))
                        i += 4
                    elif file_string[i + 1:i + 6] == "/del>":
                        token_list.append(Token(TokenType.content, content))
                        content = ""
                        token_list.append(Token(TokenType.text_del_end))
                        i += 5
                    elif file_string[i + 1:i + 6] == "code>":
                        token_list.append(Token(TokenType.content, content))
                        content = ""
                        token_list.append(Token(TokenType.text_code_begin))
                        i += 5
                    elif file_string[i + 1:i + 7] == "/code>":
                        token_list.append(Token(TokenType.content, content))
                        content = ""
                        token_list.append(Token(TokenType.text_code_end))
                        i += 6
                    elif file_string[i + 1:i + 5] == "sup>":
                        token_list.append(Token(TokenType.content, content))
                        content = ""
                        token_list.append(Token(TokenType.text_sup_begin))
                        i += 4
                    elif file_string[i + 1:i + 6] == "/sup>":
                        token_list.append(Token(TokenType.content, content))
                        content = ""
                        token_list.append(Token(TokenType.text_sup_end))
                        i += 5
                    elif file_string[i + 1:i + 5] == "sub>":
                        token_list.append(Token(TokenType.content, content))
                        content = ""
                        token_list.append(Token(TokenType.text_sub_begin))
                        i += 4
                    elif file_string[i + 1:i + 6] == "/sub>":
                        token_list.append(Token(TokenType.content, content))
                        content = ""
                        token_list.append(Token(TokenType.text_sub_end))
                        i += 5
                    i += 1
                    continue
                elif re.match(r'  \s*\*', file_string[i:]):
                    it = re.finditer(r'\*', file_string[i:])
                    for match in it:
                        off = match.start()
                        break
                    token_list.append(Token(TokenType.content, content))
                    content = ""
                    for x in range(0, off // 2):
                        token_list.append(Token(TokenType.two_spaces))
                    token_list.append(Token(TokenType.list_unord_symbol))
                    i += off + 1
                    continue
                elif re.match(r'  \s*-', file_string[i:]):
                    it = re.finditer(r'-', file_string[i:])
                    for match in it:
                        off = match.start()
                        break
                    token_list.append(Token(TokenType.content, content))
                    content = ""
                    for x in range(0, off // 2):
                        token_list.append(Token(TokenType.two_spaces))
                    token_list.append(Token(TokenType.list_ord_symbol))
                    i += off + 1
                    continue
                elif file_string[i] == "^":
                    token_list.append(Token(TokenType.content, content))
                    content = ""
                    token_list.append(Token(TokenType.tab_heading_sep))
                    i += 1
                elif file_string[i] == "|":
                    token_list.append(Token(TokenType.content, content))
                    content = ""
                    token_list.append(Token(TokenType.pipe_symbol))
                    i += 1
                elif i + 2 <= length - 1 and file_string[i] == ":" and file_string[i + 1] == ":" and file_string[i + 2] == ":":
                    token_list.append(Token(TokenType.content, content))
                    content = ""
                    token_list.append(Token(TokenType.cell_merge_symbol))
                    i += 3
                elif file_string[i] == "\n":
                    token_list.append(Token(TokenType.content, content))
                    content = ""
                    token_list.append(Token(TokenType.new_line))
                    i += 1
                elif i + 1 <= length - 1 and file_string[i] == "[" and file_string[i + 1] == "[":
                    token_list.append(Token(TokenType.content, content))
                    content = ""
                    token_list.append(Token(TokenType.link_begin))
                    i += 2
                elif i + 1 <= length - 1 and file_string[i] == "]" and file_string[i + 1] == "]":
                    token_list.append(Token(TokenType.content, content))
                    content = ""
                    token_list.append(Token(TokenType.link_end))
                    i += 2
                elif file_string[i] == "#":
                    token_list.append(Token(TokenType.content, content))
                    content = ""
                    token_list.append(Token(TokenType.link_section_sep))
                    i += 1
                elif i + 1 <= length - 1 and file_string[i] == " " and file_string[i + 1] == " ":
                    token_list.append(Token(TokenType.content, content))
                    content = ""
                    token_list.append(Token(TokenType.two_spaces))
                    i += 2
                else:
                    content += file_string[i]
                    i += 1
            content = ""
            token_list = [x for x in token_list if x.token!=TokenType.content or(x.token==TokenType.content and x.content != "")]

        return token_list