from pprint import pprint
from dokuwiki_to_html.main.parser.Parser import Parser
from dokuwiki_to_html.main.scanner.Scanner import Scanner
from dokuwiki_to_html.main.generator.Generator import Generator


scanner = Scanner()
token_list = scanner.scan('../test.txt')
parser = Parser(token_list)
pprint(token_list)
parsed_list = parser.parse()
pprint(parsed_list)
generator = Generator(parsed_list)
html_page = generator.generate_html()
print(html_page)
with open("../result.html", 'w', encoding='utf-8') as file:
    file.write(html_page)