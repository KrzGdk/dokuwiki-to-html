from pprint import pprint
from dokuwiki_to_html.main.parser.ParseError import ParseError
from dokuwiki_to_html.main.parser.Parser import Parser
from dokuwiki_to_html.main.scanner.Scanner import Scanner
from dokuwiki_to_html.main.generator.Generator import Generator


scanner = Scanner()
token_list = scanner.scan('../test.txt')
parser = Parser(token_list)
parsed_list = []
try:
    parsed_list = parser.parse()
except ParseError as e:
    print(e.value)
    exit()
except Exception:
    print("Unresolved compilation problem.")
    exit()
generator = Generator(parsed_list)
html_page = generator.generate_html()
with open("../result.html", 'w', encoding='utf-8') as file:
    file.write(html_page)

print("Compilation successful. See results in result.html file.")