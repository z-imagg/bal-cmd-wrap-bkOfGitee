from pyparsing import Word, alphas, alphanums, quotedString, Optional, Group, delimitedList,OneOrMore

def parser():
    T=alphanums + '_' + '-' + '.'
    prog=Word(alphas,alphanums+'_')
    argName1=Word('-',T)
    argVal1=quotedString  | Word(T)
    param = prog +  OneOrMore(argName1 + argVal1)
    return param




cmd = 'gcc -c User.c -o User.o'
cmd_parser=parser()
result = cmd_parser.parseString(cmd)

print(f"{result.asList()}")
# ['gcc', '-c', 'User.c', '-o', 'User.o']
