from typing import List

from lark import Lark,Transformer,Visitor
from lark.tree import Tree
from lark.visitors import Interpreter
from lark.lexer import Token



# gcc_cmd_line="  gcc -nostdlib -o arch/x86/vdso/vdso32-int80.so.dbg -fPIC -shared  -Wl,--hash-style=sysv -m32 -Wl,-soname=linux-gate.so.1 -Wl,-T,arch/x86/vdso/vdso32/vdso32.lds arch/x86/vdso/vdso32/note.o arch/x86/vdso/vdso32/int80.o"
gcc_cmd_line='gcc -Wp,-MD,arch/x86/kernel/.i8259.o.d  -nostdinc -isystem /usr/lib/gcc/i686-linux-gnu/4.4.7/include -D__KERNEL__ -Iinclude  -I/crk/bochs/linux2.6-run_at_bochs/linux-2.6.27.15/arch/x86/include -include include/linux/autoconf.h -Wall -Wundef -Wstrict-prototypes -Wno-trigraphs -fno-strict-aliasing -fno-common -Werror-implicit-function-declaration -O2 -m32 -msoft-float -mregparm=3 -freg-struct-return -mpreferred-stack-boundary=2 -march=i686 -mtune=generic -ffreestanding -pipe -Wno-sign-compare -fno-asynchronous-unwind-tables -mno-sse -mno-mmx -mno-sse2 -mno-3dnow -Iinclude/asm-x86/mach-default -Wframe-larger-than=1024 -fno-stack-protector -fno-omit-frame-pointer -fno-optimize-sibling-calls -g -pg -Wdeclaration-after-statement -Wno-pointer-sign  -D"KBUILD_STR(s)=#s" -D"KBUILD_BASENAME=KBUILD_STR(i8259)"  -D"KBUILD_MODNAME=KBUILD_STR(i8259)" -c -o arch/x86/kernel/.tmp_i8259.o arch/x86/kernel/i8259.c'


# lark.open的参数parser 取值范围 为 ('earley', 'lalr', 'cyk', None)
parser = Lark.open( 'linux_cmd.lark', rel_to=__file__, parser="earley")
# parser取 earley 或 lalr 时， Lark.open运行正常 ;
# parser取 cyk 时， Lark.open运行报错 ;

treeK:Tree = parser.parse(gcc_cmd_line)
# print(treeK.pretty())
# 提取 src_file 非终结符
# src_file = treeK.find_data('src_file')
# FILE_NAME = src_file.find_data_after('FILE_NAME')

### 用lark的Transformer访问 解析结果树 中 的 非终结符 src_file
class MyTransformer(Transformer):
    def src_file(self, tokens:List[Token]):
        #这里items确实是节点内容
        """tokens值为:
        [Token('FILE_NAME', 'arch/x86/kernel/i8259.c')]
        """
        tk=tokens[0]
        token_text:str=f"{tk.line}:{tk.column},{tk.type},{tk.value}"
        #token_text值为:    1      : 885,        FILE_NAME,arch/x86/kernel/i8259.c
        print(token_text)
        return tokens

transformer = MyTransformer()
transformer_ret = transformer.transform(treeK)
#但  transformer_ret 是 整棵结果树 ，并不是 单独该非终结符  内容

### 用lark的Interpreter访问 解析结果树 中 的 非终结符 src_file
class MyInterpreter(Interpreter):
    def src_file(self, tree):
        #这里tree确实是节点内容
        """tree值为:
        Tree(Token('RULE', 'src_file'), [Token('FILE_NAME', 'arch/x86/kernel/i8259.c')])
        """
        pass

interceptor_ret=MyInterpreter().visit(treeK)
#但  interceptor_ret 是 整棵结果树 ，并不是 单独该非终结符  内容

### 用lark的Visitor访问 解析结果树 中 的 非终结符 src_file
class MyVisitor(Visitor):
    def src_file(self, tree):
        #这里tree确实是节点内容
        """tree值为:
        Tree(Token('RULE', 'src_file'), [Token('FILE_NAME', 'arch/x86/kernel/i8259.c')])
        """
        pass

visitor_ret=MyVisitor().visit(treeK)
#但  visitor_ret 是 整棵结果树 ，并不是 单独该非终结符  内容

end=True
