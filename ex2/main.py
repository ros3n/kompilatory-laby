# coding=utf-8
import sys
import ply.yacc as yacc
from Cparser import Cparser
import TreePrinter
import AST
from Interpreter import Interpreter


from TypeChecker import TypeChecker

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "primes1.in"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)


    Cparser = Cparser()
    parser = yacc.yacc(module=Cparser, start='program')
    text = file.read()
    ast = parser.parse(text, lexer=Cparser.scanner)

    result = open("result.txt", "w")
    result.write(str(ast))
    result.close()

    tpc = ast.accept(TypeChecker())

    for word in tpc:
        print word
    if not tpc:
        ast.accept2(Interpreter())




