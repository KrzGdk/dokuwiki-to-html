from main.scanner.Scanner import Scanner


scanner = Scanner()
token_list = scanner.scan('../test.txt')
print(token_list)
