from pyparsing import Word, alphas, alphanums, quotedString, Optional, Group, delimitedList,OneOrMore,CaselessLiteral

def create_singleCmdParser():
    T=alphanums + '_-./'
    prog=Word(alphas,alphanums+'_+')
    argName1=Word('-',T)
    argName2=Word('--',T)
    argVal1=Optional(quotedString)  | Optional(Word(T))
    singleCmd = prog +  OneOrMore( (argName1|argName2) + argVal1  ) + Optional(';')
    return singleCmd




singleCmdParser=create_singleCmdParser()

cmdLs = [
'gcc --fXXX -c "My User.c" -o "User.o"',
'g++ --g --c ./common/Util.cpp -o ../build/Util.obj'
]
for cmdK in cmdLs:
    cmdKResult = singleCmdParser.parseString(cmdK)
    print(f"{cmdKResult.asList()}")

# ['gcc', '--fXXX', '-c', '"My User.c"', '-o', '"User.o"'] #命令1解析正确
# ['g++', '--g', '--c'] #错误: 命令2只解析了半截