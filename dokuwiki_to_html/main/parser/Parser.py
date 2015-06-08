from dokuwiki_to_html.main.tokens.TokenType import TokenType
from dokuwiki_to_html.main.parser.ParseError import ParseError

class Parser:

    def __init__(self,token_list):
        self.current_token = None
        self.token_list = token_list
        self.next_token_index = 0
        self.result_list = []

    def read_next_token(self):
        self.current_token = self.token_list[self.next_token_index]
        self.next_token_index += 1

    def parse(self):
        try:
            return self.do_parse()
        except:
            raise ParseError

    def do_parse(self):
        self.read_next_token()
        while self.next_token_index < len(self.token_list):
            if self.current_token.is_heading():
                self.result_list.append(self.parse_heading())
            elif self.current_token.is_formatted() or self.current_token.token == TokenType.content:
                self.result_list.append(self.parse_text())
            elif(self.current_token.token == TokenType.footnote_begin ):
                self.result_list.append(self.parse_footnote())
            elif(self.current_token.token == TokenType.link_begin ):
                self.result_list.append(self.parse_link())
            elif(self.current_token.token == TokenType.image_begin ):
                self.result_list.append(self.parse_image())
            elif(self.current_token.token == TokenType.text_code_begin ):
                self.result_list.append(self.parse_code())
            elif(self.current_token.token == TokenType.tab_heading_sep or self.current_token.token == TokenType.pipe_symbol):
                self.result_list.append(self.parse_table())
            elif self.current_token.token == TokenType.list_ord_symbol or self.current_token.token == TokenType.list_unord_symbol :
                self.result_list.append(self.parse_list())
            elif self.current_token.token == TokenType.new_line and self.token_list[self.next_token_index].token == TokenType.new_line:
                self.result_list.append({"new_paragraph"})
                self.read_next_token()
            try:
                self.read_next_token()
            except IndexError:
                break
        return self.result_list

    def parse_formatted(self):
        if(self.current_token.token == TokenType.text_del_begin ):
            self.read_next_token()
            inner_text = []
            while self.current_token.token != TokenType.text_del_end:
                inner_text.append(self.parse_text())
                self.read_next_token()
            return {'del': inner_text}
        elif(self.current_token.token == TokenType.text_monospaced_symbol ):
            self.read_next_token()
            inner_text = []
            while self.current_token.token != TokenType.text_monospaced_symbol:
                inner_text.append(self.parse_text())
                self.read_next_token()
            return {'monospaced': inner_text}
        elif(self.current_token.token == TokenType.text_underlined_symbol ):
            self.read_next_token()
            inner_text = []
            while self.current_token.token != TokenType.text_underlined_symbol:
                inner_text.append(self.parse_text())
                self.read_next_token()
            return {'underlined': inner_text}
        elif(self.current_token.token == TokenType.text_bold_symbol ):
            self.read_next_token()
            inner_text = []
            while self.current_token.token != TokenType.text_bold_symbol:
                inner_text.append(self.parse_text())
                self.read_next_token()
            return {'bold': inner_text}
        elif(self.current_token.token == TokenType.text_italics_symbol ):
            self.read_next_token()
            inner_text = []
            while self.current_token.token != TokenType.text_italics_symbol:
                inner_text.append(self.parse_text())
                self.read_next_token()
            return {'italics': inner_text}
        elif(self.current_token.token == TokenType.text_sup_begin ):
            self.read_next_token()
            inner_text = []
            while self.current_token.token != TokenType.text_sup_end:
                inner_text.append(self.parse_text())
                self.read_next_token()
            return {'sup': inner_text}
        elif(self.current_token.token == TokenType.text_sub_begin ):
            self.read_next_token()
            inner_text = []
            while self.current_token.token != TokenType.text_sub_end:
                inner_text.append(self.parse_text())
                self.read_next_token()
            return {'sub': inner_text}

    def parse_code(self):
        self.read_next_token()
        inner_text = []
        while self.current_token.token != TokenType.text_code_end:
            if self.current_token.token == TokenType.two_spaces:
                inner_text.append("  ")
            if self.current_token.token == TokenType.new_line:
                inner_text.append("\n")
            inner_text.append(self.parse_unformatted())
            self.read_next_token()
        return {'code': inner_text}

    def parse_footnote(self):
        if(self.current_token.token == TokenType.footnote_begin ):
            self.read_next_token()
            inner_text = self.parse_unformatted()
            self.read_next_token()
            if self.current_token.token != TokenType.footnote_end:
                raise ParseError
            return {'footnote': inner_text}

    def get_alignment(self, cell_text):
        left_side = True
        left_double_spaces = 0
        right_double_spaces = 0
        for i in cell_text:
            if hasattr(i, 'token') and i.token == TokenType.two_spaces and left_side:
                left_double_spaces += 1
            if hasattr(i, 'token') and i.token == TokenType.two_spaces and not left_side:
                right_double_spaces += 1
            if not hasattr(i, 'token') or (i.token != TokenType.two_spaces and left_side):
                left_side = False
            if not hasattr(i, 'token') or (i.token != TokenType.two_spaces and not left_side):
                right_double_spaces = 0
        if left_double_spaces >= 1 and right_double_spaces >= 1:
            align = "center"
        elif left_double_spaces >= 1 and right_double_spaces == 0:
            align = "right"
        else:
            align = "left"
        return align

    def parse_table(self):
        rows = []
        while True:
            if self.current_token.token == TokenType.new_line:
                self.read_next_token()
            row = []
            while self.current_token.token != TokenType.new_line:
                if self.current_token.token == TokenType.tab_heading_sep and self.current_token.token != TokenType.new_line:
                    self.read_next_token()
                    cell_text = []
                    while self.current_token.token not in [TokenType.tab_heading_sep, TokenType.pipe_symbol, TokenType.new_line]:
                        if self.current_token.token == TokenType.cell_merge_symbol:
                            cell_text.append({"cell_merge"})
                        elif self.current_token.is_formatted() or self.current_token.token==TokenType.content:
                            cell_text.append(self.parse_text())
                        elif self.current_token.token == TokenType.two_spaces:
                            cell_text.append(self.current_token)
                        self.read_next_token()
                    if self.current_token.token != TokenType.new_line:
                        cell_text = [x for x in cell_text if x != " "]
                        align = self.get_alignment(cell_text)
                        row.append({'th': [i for i in cell_text if not hasattr(i,'token') or i.token != TokenType.two_spaces], 'align': align})

                elif self.current_token.token == TokenType.pipe_symbol and self.current_token.token != TokenType.new_line:
                    self.read_next_token()
                    cell_text = []
                    while self.current_token.token not in [TokenType.tab_heading_sep, TokenType.pipe_symbol, TokenType.new_line]:
                        if self.current_token.token == TokenType.cell_merge_symbol:
                            cell_text.append({"cell_merge"})
                        elif self.current_token.is_formatted() or self.current_token.token==TokenType.content:
                            cell_text.append(self.parse_text())
                        elif self.current_token.token == TokenType.two_spaces:
                            cell_text.append(self.current_token)
                        self.read_next_token()
                    if self.current_token.token != TokenType.new_line:
                        cell_text = [x for x in cell_text if x != " "]
                        align = self.get_alignment(cell_text)
                        row.append({'td': [i for i in cell_text if not hasattr(i,'token') or i.token != TokenType.two_spaces], 'align': align})
            rows.append(row)
            if self.current_token.token == TokenType.new_line \
                    and self.token_list[self.next_token_index].token not in [TokenType.tab_heading_sep, TokenType.pipe_symbol]:
                break
        return {'table': rows}

    def parse_ord_list(self,indents):
        item_content = []
        self.read_next_token()
        while self.current_token.token != TokenType.new_line:
            if self.current_token.is_formatted() or self.current_token.token==TokenType.content:
                item_content.append(self.parse_text())
            else:
                raise ParseError
            self.read_next_token()
        return {'ol.li': item_content, 'level' : indents}

    def parse_unord_list(self,indents):
        item_content = []
        self.read_next_token()
        while self.current_token.token != TokenType.new_line:
            if self.current_token.is_formatted() or self.current_token.token==TokenType.content:
                item_content.append(self.parse_text())
            else:
                raise ParseError
            self.read_next_token()
        return {'ul.li': item_content, 'level' : indents}

    def parse_image(self):
        self.read_next_token()
        link_text = ""
        while self.current_token.token != TokenType.image_end:
            link_text += self.current_token.content
            self.read_next_token()
        link_parts = link_text.partition("?")
        link = link_parts[0]
        if link_parts[2] != "":
            (width, x, height) = tuple(link_parts[2].partition("x"))
            width = ''.join(filter(lambda x: x.isdigit(), width))
            height = ''.join(filter(lambda x: x.isdigit(), height))
            if height != "":
                return {'img': {'src': link, 'height': height, 'width': width}}
            return {'img': {'src': link, 'width': width}}
        return {'img': {'src': link}}


    def parse_link(self):
        self.read_next_token()
        link_url = ""
        link_content = ""
        while self.current_token.token not in [TokenType.pipe_symbol, TokenType.link_end]:
            link_url += self.current_token.content
            self.read_next_token()
        if self.current_token.token == TokenType.pipe_symbol:
            self.read_next_token()
            if self.current_token.token == TokenType.content:
                while self.current_token.token != TokenType.link_end:
                    link_content += self.current_token.content
                    self.read_next_token()
            elif self.current_token.token == TokenType.image_begin:
                link_content = self.parse_image()
            else:
                raise ParseError
        return {'link': {'url': link_url, 'content': link_content}}

    def parse_text(self):
        if self.current_token.is_formatted():
            return self.parse_formatted()
        else:
            return self.parse_unformatted()

    def parse_heading(self):
        if(self.current_token.token == TokenType.heading_level1 ):
            self.read_next_token()
            inner_text = self.parse_unformatted()
            self.read_next_token()
            if self.current_token.token != TokenType.heading_level1:
                raise ParseError
            return {'h1': inner_text}
        elif(self.current_token.token == TokenType.heading_level2 ):
            self.read_next_token()
            inner_text = self.parse_unformatted()
            self.read_next_token()
            if self.current_token.token != TokenType.heading_level2:
                raise ParseError
            return {'h2': inner_text}
        elif(self.current_token.token == TokenType.heading_level3 ):
            self.read_next_token()
            inner_text = self.parse_unformatted()
            self.read_next_token()
            if self.current_token.token != TokenType.heading_level3:
                raise ParseError
            return {'h3': inner_text}
        elif(self.current_token.token == TokenType.heading_level4 ):
            self.read_next_token()
            inner_text = self.parse_unformatted()
            self.read_next_token()
            if self.current_token.token != TokenType.heading_level4:
                raise ParseError
            return {'h4': inner_text}
        elif(self.current_token.token == TokenType.heading_level5 ):
            self.read_next_token()
            inner_text = self.parse_unformatted()
            self.read_next_token()
            if self.current_token.token != TokenType.heading_level5:
                raise ParseError
            return {'h5': inner_text}
        elif(self.current_token.token == TokenType.heading_level6 ):
            self.read_next_token()
            inner_text = self.parse_unformatted()
            self.read_next_token()
            if self.current_token.token != TokenType.heading_level6:
                raise ParseError
            return {'h6': inner_text}

    def parse_unformatted(self):
        return self.current_token.content

    def parse_list(self):
        indents = 0
        i = self.next_token_index - 2
        while True:
            temp_token = self.token_list[i]
            if temp_token.token == TokenType.two_spaces:
                indents += 1
            i -= 1
            if temp_token.token != TokenType.two_spaces:
                break
        if self.current_token.token == TokenType.list_ord_symbol or self.current_token.token == TokenType.list_unord_symbol:
            items = []
            while True:
                if self.current_token.token == TokenType.list_ord_symbol:
                    items.append(self.parse_ord_list(indents))
                elif self.current_token.token == TokenType.list_unord_symbol:
                    items.append(self.parse_unord_list(indents))

                self.read_next_token()
                while self.current_token.token == TokenType.two_spaces:
                    self.read_next_token()

                if self.current_token.token == TokenType.list_ord_symbol or self.current_token.token == TokenType.list_unord_symbol:
                    indents = 0
                    i = self.next_token_index - 2
                    while True:
                        temp_token = self.token_list[i]
                        if temp_token.token == TokenType.two_spaces:
                            indents += 1
                        i -= 1
                        if temp_token.token != TokenType.two_spaces:
                            break
                else:
                    self.current_token = self.token_list[self.next_token_index-2]
                    self.next_token_index -= 1
                    break
        return {'list': items}

