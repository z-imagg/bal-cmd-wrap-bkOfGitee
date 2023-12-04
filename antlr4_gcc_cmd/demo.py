from antlr4 import CommonTokenStream, ParseTreeWalker, InputStream

from parser_generated.SingleCmdParser import SingleCmdParser
from parser_generated.SingleCmdLexer import  SingleCmdLexer
from parser_generated.SingleCmdListener import SingleCmdListener

class HelloPrintListener(SingleCmdListener):
    def enterProgram(self, ctx:SingleCmdParser.ProgramContext):
        # 函数名enterR的R指的是非终结符r
        print("program: %s" % ctx.getText())
        #输出为:  program: cxx


cmdLn='cxx   -c -o arch/x86/kernel/.tmp_i8259.o arch/x86/kernel/i8259.c'

input_stream = InputStream(cmdLn)
lexer = SingleCmdLexer(input_stream)
stream = CommonTokenStream(lexer)
parser = SingleCmdParser(stream)
tree = parser.singleCmd()
# tree = parser.r()
printer = HelloPrintListener()
walker = ParseTreeWalker()
walker.walk(printer, tree)


