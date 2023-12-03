from antlr4 import CommonTokenStream, ParseTreeWalker, InputStream

from antlr4_gcc_cmd.parser_generated.SingleCmdParser import SingleCmdParser
from antlr4_gcc_cmd.parser_generated.SingleCmdLexer import  SingleCmdLexer
from antlr4_gcc_cmd.parser_generated.SingleCmdParserListener import SingleCmdParserListener

class HelloPrintListener(SingleCmdParserListener):
    def enterSrc_file(self, ctx:SingleCmdParser.Src_fileContext):
        # 函数名enterR的R指的是非终结符r
        print("src_file: %s" % ctx.ID())


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


