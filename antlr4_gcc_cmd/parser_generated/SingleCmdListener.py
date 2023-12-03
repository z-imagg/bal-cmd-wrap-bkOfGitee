# Generated from SingleCmd.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .SingleCmdParser import SingleCmdParser
else:
    from SingleCmdParser import SingleCmdParser

# This class defines a complete listener for a parse tree produced by SingleCmdParser.
class SingleCmdListener(ParseTreeListener):

    # Enter a parse tree produced by SingleCmdParser#singleCmd.
    def enterSingleCmd(self, ctx:SingleCmdParser.SingleCmdContext):
        pass

    # Exit a parse tree produced by SingleCmdParser#singleCmd.
    def exitSingleCmd(self, ctx:SingleCmdParser.SingleCmdContext):
        pass


    # Enter a parse tree produced by SingleCmdParser#program.
    def enterProgram(self, ctx:SingleCmdParser.ProgramContext):
        pass

    # Exit a parse tree produced by SingleCmdParser#program.
    def exitProgram(self, ctx:SingleCmdParser.ProgramContext):
        pass


    # Enter a parse tree produced by SingleCmdParser#av_pairs.
    def enterAv_pairs(self, ctx:SingleCmdParser.Av_pairsContext):
        pass

    # Exit a parse tree produced by SingleCmdParser#av_pairs.
    def exitAv_pairs(self, ctx:SingleCmdParser.Av_pairsContext):
        pass


    # Enter a parse tree produced by SingleCmdParser#av_pair.
    def enterAv_pair(self, ctx:SingleCmdParser.Av_pairContext):
        pass

    # Exit a parse tree produced by SingleCmdParser#av_pair.
    def exitAv_pair(self, ctx:SingleCmdParser.Av_pairContext):
        pass


    # Enter a parse tree produced by SingleCmdParser#arg.
    def enterArg(self, ctx:SingleCmdParser.ArgContext):
        pass

    # Exit a parse tree produced by SingleCmdParser#arg.
    def exitArg(self, ctx:SingleCmdParser.ArgContext):
        pass


    # Enter a parse tree produced by SingleCmdParser#value.
    def enterValue(self, ctx:SingleCmdParser.ValueContext):
        pass

    # Exit a parse tree produced by SingleCmdParser#value.
    def exitValue(self, ctx:SingleCmdParser.ValueContext):
        pass


    # Enter a parse tree produced by SingleCmdParser#word.
    def enterWord(self, ctx:SingleCmdParser.WordContext):
        pass

    # Exit a parse tree produced by SingleCmdParser#word.
    def exitWord(self, ctx:SingleCmdParser.WordContext):
        pass



del SingleCmdParser