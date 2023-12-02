from pyparsing import Word, alphas, alphanums, quotedString, Optional, Group, delimitedList

def parser():
    T=alphanums + '_' + '-'
    prog=Word(alphas,alphanums+'_')
    argName1=Word('-',T)
    argVal1=quotedString  | Word(T)
    param = prog +  argName1 + argVal1
    command_parser = delimitedList(param)
    return command_parser




# 示例命令
# cmd = 'command -param1 value1 --p2 "Val2"  param5'
# cmd = 'command --p2 "Val2"  param5'
cmd = 'command -p2 Val2'
# 解析命令
command_parser=parser()
prog,argName1,argVal1 = command_parser.parseString(cmd)

print(f"prog:{prog},参数名: {argName1}, 值: {argVal1}")
# prog:command,参数名: -p2, 值: Val2
