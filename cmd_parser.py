from pyparsing import Word, alphas, alphanums, quotedString, Optional, Group, delimitedList,OneOrMore,CaselessLiteral

def create_singleCmdParser():
    T=alphanums + '_-./'
    prog=Word(alphas,alphanums+'_+')
    argName1=Word('-',T)
    argName2=Word('--',T)
    argVal1=quotedString  | Word(T)
    singleCmd = prog +  OneOrMore( (argName1|argName2) + Optional(argVal1)  ) + Optional(';')
    return singleCmd




singleCmdParser=create_singleCmdParser()

cmdLs = [
'gcc --fXXX -c "My User.c" -o "User.o"',
'g++ --g --c ./common/Util.cpp -o ../build/Util.obj'
]
for cmdK in cmdLs:
    cmdKResult = singleCmdParser.parse_string(cmdK)
    # print(cmdKResult.dump())
    print(f"{cmdKResult.asList()}")
    break

# ['gcc', '--fXXX', 'yes', '-c', '"My User.c"', '-o', '"User.o"']
# ['g++', '-c', './common/Util.cpp', '-o', '../build/Util.obj']