from pprint import pprint
from dokuwiki_to_html.main.parser.Parser import Parser
from dokuwiki_to_html.main.scanner.Scanner import Scanner


scanner = Scanner()
token_list = scanner.scan('../test.txt')
parser = Parser(token_list)
parsed_list = parser.parse();
pprint(parsed_list)