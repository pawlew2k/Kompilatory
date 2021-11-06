# DO USUNIĘCIA GDY SCANNER BĘDZIE PEWNY

# import sys
# import scanner  # scanner.py is a file you create, (it is not an external library)
#
# if __name__ == '__main__':
#
#     try:
#         filename = sys.argv[1] if len(sys.argv) > 1 else "../utils/text.txt"
#         file = open(filename, "r")
#     except IOError:
#         print("Cannot open {0} file".format(filename))
#         sys.exit(0)
#
#     text = file.read()
#     lexer = scanner.lexer
#     lexer.input(text)  # Give the lexer some input
#
#     # Tokenize
#     while True:
#         tok = lexer.token()
#         if not tok:
#             break    # No more input
#         print("(%d): %s(%s)" % (tok.lineno, tok.type, tok.value))

import sys
import scanner
import Mparser

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "../utils/test.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = Mparser.parser
    text = file.read()
    parser.parse(text, lexer=scanner.lexer)