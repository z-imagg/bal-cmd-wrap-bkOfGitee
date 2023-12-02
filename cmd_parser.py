from pyparsing import Word, alphas, alphanums, quotedString, Optional, Group, delimitedList,OneOrMore,CaselessLiteral

def create_singleCmdParser():
    T=alphanums + '_-./'
    prog=Word(alphas,alphanums+'_+')
    argName1=Word('-',T)
    argName2=Word('--',T)
    argVal1=Optional(Word(T)) | Optional(quotedString)  
    singleCmd = prog +  OneOrMore( (argName1|argName2) + argVal1  ) + Optional(';')
    return singleCmd




singleCmdParser=create_singleCmdParser()

cmdLs = [
'gcc --fXXX -c "My User.c" -o "User.o"',
'g++  --c ./common/Util.cpp --o ../build/Util.obj'
]
for cmdK in cmdLs:
    cmdKResult = singleCmdParser.parseString(cmdK)
    print(f"{cmdKResult.asList()}")

# ['gcc', '--fXXX', '-c'] #错误: 命令1只解析了半截
# ['g++', '--c', './common/Util.cpp', '--o', '../build/Util.obj'] #命令2解析正确