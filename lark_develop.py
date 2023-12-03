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
print(treeK.pretty())

################获取 结果树 中的 src_file 非终结符 节点 的 值
src_file_ls=[]
### 用lark的Transformer访问 解析结果树 中 的 非终结符 src_file
class MyTransformer(Transformer):
    def src_file(self, tokens:List[Token]):
        #这里items确实是节点内容
        """tokens值为:
        [Token('FILE_NAME', 'arch/x86/kernel/i8259.c')]
        """
        src_file_ls.append(tokens)
        return tokens

transformer = MyTransformer()
transformer_ret = transformer.transform(treeK)
#但  transformer_ret 是 整棵结果树 ，并不是 单独该非终结符  内容


assert len(src_file_ls) <= 1
#一条gcc命令中不会有多个 源文件

if len(src_file_ls) == 1:
    src_file_tokens:List[Token]=src_file_ls[0]
    src_file:Token=src_file_tokens[0]
    assert src_file.type=='FILE_NAME'
    src_file_val:str=src_file.value
    print(f"命令中的源文件为:{src_file_val}")

end=True
