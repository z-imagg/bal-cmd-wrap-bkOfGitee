from pyparsing import Word, alphas, alphanums, QuotedString, Optional, Group, delimitedList

def parse_command(command):
    # 定义语法规则
    T=alphanums + '_' + '-'
    ID=Word(alphas,T)
    param_name_1=Word('-',T)
    param_name_2=Word('--',T)
    param_name = ID | param_name_1 | param_name_2
    param_value = QuotedString(quoteChar='"') | QuotedString(quoteChar="'") | Word(T)
    param = Group(param_name + Optional("=") + Optional(param_value) ) | param_value
    command_parser = delimitedList(param)

    # 解析命令
    parsed_params = command_parser.parseString(command)

    # 输出参数名和值
    for param in parsed_params:
        param_name = param[0] if len(param) > 0 else ""
        param_value = param[1] if len(param) > 1 else ""
        print(f"参数名: {param_name}, 值: {param_value}")

# 示例命令
# example_command = 'command -param1 value1 --p2 "Val2"  param5'
example_command = 'command --p2 "Val2"  param5'

# 调用函数解析命令
parse_command(example_command)