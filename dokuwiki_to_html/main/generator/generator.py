from _operator import itemgetter
import html


class Generator:
    def __init__(self, struct):
        self.formattings = ['del', 'bold', 'italics', 'sup', 'sub', 'underlined', 'monospaced']
        self.html_page = ""
        self.struct = struct
        self.footnote_count = 0
        self.footnotes = []

    def generate_html(self):
        self._generate_headers()
        for item in self.struct:
            self._append_item(item)

        self._append_hr()
        self._append_footnotes()
        self._generate_footer()
        return self.html_page

    def _append_item(self, item):
        if isinstance(item, set):
            if 'new_paragraph' in item:
                self.html_page += "</p>\n<p>"
        if not isinstance(item, set) and not isinstance(item, str):
            (k, v) = item.popitem()
            if k in ['h1', 'h2', 'h3', 'h4', 'h5']:
                self._append_h_tag(k, v)
            elif k in self.formattings:
                self._append_formatted(k, v)
            elif k == 'code':
                self._append_code(v)
            elif k == 'list':
                self._append_list(v)
            elif k == 'link':
                self._append_link(v)
            elif k == 'img':
                self._append_image(v)
            elif k == 'footnote':
                self._append_footnote(v)
            elif k == 'table':
                self._append_table(v)
        elif isinstance(item, str):
            self._append_unformatted(item)

    def _append_h_tag(self, tag, text):
        elem = "<" + tag + ">"
        elem += text
        elem += "</" + tag + ">"
        self.html_page += elem

    def _generate_headers(self):
        self.html_page += "<html>\n<head>\n</head>\n<body>\n<p>\n"

    def _generate_footer(self):
        self.html_page += "</p>\n</body>\n</html>"

    def _append_unformatted(self, text):
        self.html_page += text

    def _append_formatted(self, tag, content):
        self.html_page += "<" + self._to_html_tag(tag) + ">"
        for item in content:
            self._append_formatted_or_unformatted(item)
        self.html_page += "</" + self._to_html_tag(tag) + ">"

    def _append_formatted_or_unformatted(self, content):
        if isinstance(content, str):
            self._append_unformatted(content)
        else:
            (tag, inner) = content.popitem()
            self._append_formatted(tag, inner)

    def _append_formatted_or_unformatted_list(self, content_list):
        for content in content_list:
            self._append_formatted_or_unformatted(content)

    def _to_html_tag(self, tag):
        if tag == 'bold':
            return 'strong'
        elif tag == 'italics':
            return 'em'
        elif tag == 'underlined':
            return 'u'
        elif tag == 'del':
            return 'strike'
        elif tag == 'monospaced':
            return 'code'
        else:
            return tag

    def _append_list(self, item_list):
        last_level = 0
        last_list_type = ''
        lists_to_close = []
        for item in item_list:
            if 'ul.li' in item.keys():
                list_type = 'ul'
            else:
                list_type = 'ol'
            if item['level'] > last_level:
                lists_to_close.append(list_type)
                self.html_page += "<" + list_type + ">"
                last_level = item['level']
                last_list_type = list_type
            elif item['level'] < last_level:
                level_diff = last_level - item['level']
                for one_level_diff in range(0, level_diff):
                    self.html_page += "</" + lists_to_close.pop() + ">"
                last_level = item['level']
                last_list_type = list_type

            self.html_page += "<li>"
            self._append_formatted_or_unformatted_list(item[list_type + '.li'])

        while len(lists_to_close) > 0:
            self.html_page += "</" + lists_to_close.pop() + ">"

    def _append_link(self, link):
        self.html_page += "<a href=\"" + link['url'] + "\">"
        if isinstance(link['content'], str):
            self._append_formatted_or_unformatted(link['content'])
        else:
            self._append_image(link['content']['img'])
        self.html_page += "</a>"

    def _append_image(self, img):
        self.html_page += "<img src=\"" + img['src'] + "\" style=\""
        if 'height' in img:
            self.html_page += "height:" + img['height'] + "px;"
        if 'width' in img:
            self.html_page += "width:" + img['width'] + "px"
        self.html_page += "\" />"

    def _append_footnote(self, v):
        self.footnote_count += 1
        self.html_page += "<sup><a href=\"#fn" + str(self.footnote_count) + "\" id=\"ref" + str(self.footnote_count) \
                          + "\">" + str(self.footnote_count) + ")</a></sup>"
        self.footnotes.append(v)

    def _append_footnotes(self):
        self.html_page += "</p><p>"
        for i, footnote in enumerate(self.footnotes):
            idx = str(i + 1)
            self.html_page += "<sup id=\"fn" + idx + "\">"
            self.html_page += idx + ") </sup>"
            self.html_page += footnote
            self.html_page += "<a href=\"#ref" + idx + "\" "
            self.html_page += "title=\"Skocz do przypisu " + idx + ".\">^</a></sup>"

    def _append_hr(self):
        self.html_page += "<hr/>"

    def _append_table(self, v):
        numrows = len(v)
        if numrows < 1:
            return
        numcols = len(v[0])
        self.html_page += '<table>'
        merged_cells = []
        for r, row in enumerate(v):
            for c, col in enumerate(row):
                if 'th' in col:
                    for s in col['th']:
                        if isinstance(s, set):
                            merged_cells.append((r, c))
                elif 'td' in col:
                    for s in col['td']:
                        if isinstance(s, set):
                            merged_cells.append((r, c))

        for r, row in enumerate(v):
            self.html_page += '<tr>'
            for c, col in enumerate(row):
                if (r, c) in merged_cells:
                    continue
                rowspan = 1
                nextrow = r + 1
                if (nextrow, c) in merged_cells:
                    rowspan = 2
                    nextrow += 1
                    while (nextrow, c) in merged_cells:
                        rowspan += 1
                        nextrow += 1
                align = col['align']
                if 'th' in col:
                    self.html_page += '<th rowspan=' + str(
                        rowspan) + ' style="text-align:' + align + ';vertical-align:top">'
                    self._append_formatted_or_unformatted_list(col['th'])
                    self.html_page += '</th>'
                elif 'td' in col:
                    self.html_page += '<td rowspan=' + str(
                        rowspan) + ' style="text-align:' + align + ';vertical-align:top">'
                    self._append_formatted_or_unformatted_list(col['td'])
                    self.html_page += '</td>'
        self.html_page += '</table>'

    def _append_code(self, v):
        self.html_page += "<pre>"
        self._append_formatted_or_unformatted_list(v)
        self.html_page += "</pre>"