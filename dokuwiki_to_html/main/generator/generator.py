from _operator import itemgetter
import html


class Generator:
    def __init__(self, struct):
        self.formattings = ['del', 'bold', 'italics', 'sup', 'sub', 'underlined', 'monospaced']
        self.html_page = ""
        self.struct = struct

    def generate_html(self):
        self._generate_headers()
        for item in self.struct:
            self._append_item(item)

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
            elif k == 'list':
                self._append_list(v)
            elif k == 'table':
                pass
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