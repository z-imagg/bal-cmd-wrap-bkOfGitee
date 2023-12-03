# Generated from SingleCmd.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,11,62,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,1,0,1,0,4,0,17,8,0,11,0,12,0,18,1,0,5,0,22,8,0,10,0,12,0,25,9,
        0,1,0,3,0,28,8,0,1,0,1,0,1,1,1,1,1,2,1,2,4,2,36,8,2,11,2,12,2,37,
        1,2,5,2,41,8,2,10,2,12,2,44,9,2,1,3,1,3,1,3,3,3,49,8,3,1,3,1,3,1,
        3,3,3,54,8,3,1,4,1,4,1,5,1,5,1,6,1,6,1,6,0,0,7,0,2,4,6,8,10,12,0,
        1,1,0,4,5,61,0,14,1,0,0,0,2,31,1,0,0,0,4,33,1,0,0,0,6,53,1,0,0,0,
        8,55,1,0,0,0,10,57,1,0,0,0,12,59,1,0,0,0,14,16,3,2,1,0,15,17,5,1,
        0,0,16,15,1,0,0,0,17,18,1,0,0,0,18,16,1,0,0,0,18,19,1,0,0,0,19,23,
        1,0,0,0,20,22,3,4,2,0,21,20,1,0,0,0,22,25,1,0,0,0,23,21,1,0,0,0,
        23,24,1,0,0,0,24,27,1,0,0,0,25,23,1,0,0,0,26,28,5,2,0,0,27,26,1,
        0,0,0,27,28,1,0,0,0,28,29,1,0,0,0,29,30,5,0,0,1,30,1,1,0,0,0,31,
        32,5,6,0,0,32,3,1,0,0,0,33,42,3,6,3,0,34,36,5,1,0,0,35,34,1,0,0,
        0,36,37,1,0,0,0,37,35,1,0,0,0,37,38,1,0,0,0,38,39,1,0,0,0,39,41,
        3,6,3,0,40,35,1,0,0,0,41,44,1,0,0,0,42,40,1,0,0,0,42,43,1,0,0,0,
        43,5,1,0,0,0,44,42,1,0,0,0,45,48,3,8,4,0,46,47,5,3,0,0,47,49,3,10,
        5,0,48,46,1,0,0,0,48,49,1,0,0,0,49,54,1,0,0,0,50,51,3,8,4,0,51,52,
        5,4,0,0,52,54,1,0,0,0,53,45,1,0,0,0,53,50,1,0,0,0,54,7,1,0,0,0,55,
        56,5,5,0,0,56,9,1,0,0,0,57,58,3,12,6,0,58,11,1,0,0,0,59,60,7,0,0,
        0,60,13,1,0,0,0,7,18,23,27,37,42,48,53
    ]

class SingleCmdParser ( Parser ):

    grammarFileName = "SingleCmd.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "' '", "';'", "'='" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "QUOTED_STRING", "TOKEN", "FILE_NAME", "FILE_NAME_LEAD", 
                      "FILE_NAME_MID", "DIGIT", "LETTER", "WS" ]

    RULE_singleCmd = 0
    RULE_program = 1
    RULE_av_pairs = 2
    RULE_av_pair = 3
    RULE_arg = 4
    RULE_value = 5
    RULE_word = 6

    ruleNames =  [ "singleCmd", "program", "av_pairs", "av_pair", "arg", 
                   "value", "word" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    QUOTED_STRING=4
    TOKEN=5
    FILE_NAME=6
    FILE_NAME_LEAD=7
    FILE_NAME_MID=8
    DIGIT=9
    LETTER=10
    WS=11

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class SingleCmdContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def program(self):
            return self.getTypedRuleContext(SingleCmdParser.ProgramContext,0)


        def EOF(self):
            return self.getToken(SingleCmdParser.EOF, 0)

        def av_pairs(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SingleCmdParser.Av_pairsContext)
            else:
                return self.getTypedRuleContext(SingleCmdParser.Av_pairsContext,i)


        def getRuleIndex(self):
            return SingleCmdParser.RULE_singleCmd

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSingleCmd" ):
                listener.enterSingleCmd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSingleCmd" ):
                listener.exitSingleCmd(self)




    def singleCmd(self):

        localctx = SingleCmdParser.SingleCmdContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_singleCmd)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 14
            self.program()
            self.state = 16 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 15
                self.match(SingleCmdParser.T__0)
                self.state = 18 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==1):
                    break

            self.state = 23
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==5:
                self.state = 20
                self.av_pairs()
                self.state = 25
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 27
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==2:
                self.state = 26
                self.match(SingleCmdParser.T__1)


            self.state = 29
            self.match(SingleCmdParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FILE_NAME(self):
            return self.getToken(SingleCmdParser.FILE_NAME, 0)

        def getRuleIndex(self):
            return SingleCmdParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)




    def program(self):

        localctx = SingleCmdParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_program)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 31
            self.match(SingleCmdParser.FILE_NAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Av_pairsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def av_pair(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SingleCmdParser.Av_pairContext)
            else:
                return self.getTypedRuleContext(SingleCmdParser.Av_pairContext,i)


        def getRuleIndex(self):
            return SingleCmdParser.RULE_av_pairs

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAv_pairs" ):
                listener.enterAv_pairs(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAv_pairs" ):
                listener.exitAv_pairs(self)




    def av_pairs(self):

        localctx = SingleCmdParser.Av_pairsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_av_pairs)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 33
            self.av_pair()
            self.state = 42
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1:
                self.state = 35 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 34
                    self.match(SingleCmdParser.T__0)
                    self.state = 37 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==1):
                        break

                self.state = 39
                self.av_pair()
                self.state = 44
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Av_pairContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def arg(self):
            return self.getTypedRuleContext(SingleCmdParser.ArgContext,0)


        def value(self):
            return self.getTypedRuleContext(SingleCmdParser.ValueContext,0)


        def QUOTED_STRING(self):
            return self.getToken(SingleCmdParser.QUOTED_STRING, 0)

        def getRuleIndex(self):
            return SingleCmdParser.RULE_av_pair

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAv_pair" ):
                listener.enterAv_pair(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAv_pair" ):
                listener.exitAv_pair(self)




    def av_pair(self):

        localctx = SingleCmdParser.Av_pairContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_av_pair)
        self._la = 0 # Token type
        try:
            self.state = 53
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 45
                self.arg()
                self.state = 48
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==3:
                    self.state = 46
                    self.match(SingleCmdParser.T__2)
                    self.state = 47
                    self.value()


                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 50
                self.arg()
                self.state = 51
                self.match(SingleCmdParser.QUOTED_STRING)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TOKEN(self):
            return self.getToken(SingleCmdParser.TOKEN, 0)

        def getRuleIndex(self):
            return SingleCmdParser.RULE_arg

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArg" ):
                listener.enterArg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArg" ):
                listener.exitArg(self)




    def arg(self):

        localctx = SingleCmdParser.ArgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_arg)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 55
            self.match(SingleCmdParser.TOKEN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def word(self):
            return self.getTypedRuleContext(SingleCmdParser.WordContext,0)


        def getRuleIndex(self):
            return SingleCmdParser.RULE_value

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValue" ):
                listener.enterValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValue" ):
                listener.exitValue(self)




    def value(self):

        localctx = SingleCmdParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_value)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 57
            self.word()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WordContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TOKEN(self):
            return self.getToken(SingleCmdParser.TOKEN, 0)

        def QUOTED_STRING(self):
            return self.getToken(SingleCmdParser.QUOTED_STRING, 0)

        def getRuleIndex(self):
            return SingleCmdParser.RULE_word

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWord" ):
                listener.enterWord(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWord" ):
                listener.exitWord(self)




    def word(self):

        localctx = SingleCmdParser.WordContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_word)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 59
            _la = self._input.LA(1)
            if not(_la==4 or _la==5):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





