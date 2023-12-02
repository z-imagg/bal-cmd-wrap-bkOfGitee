from pyparsing import Word, alphas, alphanums, quotedString, Optional, Group, delimitedList,OneOrMore

def create_singleCmdParser():
    T=alphanums + '_' + '-' + '.'
    prog=Word(alphas,alphanums+'_')
    argName1=Word('-',T)
    argVal1=quotedString  | Word(T)
    singleCmd = prog +  OneOrMore(argName1 + argVal1)
    return singleCmd




singleCmd = 'gcc -c "My User.c" -o "User.o"'
singleCmdParser=create_singleCmdParser()
parse_result = singleCmdParser.parseString(singleCmd)

print(f"{parse_result.asList()}")
#['gcc', '-c', '"My User.c"', '-o', '"User.o"']
