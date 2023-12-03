from lark import Lark

grammar = '''
grammar singleCmd;

singleCmd: program av_pairs* ";";

program: FILE_NAME;

av_pairs: av_pair+;

av_pair: arg "="? value | arg QUOTED_STRING;

arg: TOKEN;

value: word;

word: TOKEN | QUOTED_STRING;

QUOTED_STRING: /"([^"\n])*"/ | /'([^'\n])*'/;

TOKEN: /[0-9a-zA-Z.\-\/_:,]+/;

FILE_NAME: (FILE_NAME_LEAD | DIGIT | LETTER) (FILE_NAME_MID | DIGIT | LETTER)+;

FILE_NAME_LEAD: "." | "_" | "," | "+";

FILE_NAME_MID: FILE_NAME_LEAD | "-";

DIGIT: /[0-9]/;

LETTER: /[a-zA-Z]/;

%ignore WS;
'''

input_string = 'gcc -Wp,-MD,arch/x86/mm/.pgtable.o.d -nostdinc -isystem /usr/lib/gcc/i686-linux-gnu/4.4.7/include -D__KERNEL__ -Iinclude -I/crk/bochs/linux2.6-run_at_bochs/linux-2.6.27.15/arch/x86/include -include include/linux/autoconf.h -Wall -Wundef -Wstrict-prototypes -Wno-trigraphs -fno-strict-aliasing -fno-common -Werror-implicit-function-declaration -O2 -m32 -msoft-float -mregparm=3 -freg-struct-return -mpreferred-stack-boundary=2 -march=i686 -mtune=generic -ffreestanding -pipe -Wno-sign-compare -fno-asynchronous-unwind-tables -mno-sse -mno-mmx -mno-sse2 -mno-3dnow -Iinclude/asm-x86/mach-default -Wframe-larger-than=1024 -fno-stack-protector -fno-omit-frame-pointer -fno-optimize-sibling-calls -g -pg -Wdeclaration-after-statement -Wno-pointer-sign -D"KBUILD_STR(s)=#s" -D"KBUILD_BASENAME=KBUILD_STR(pgtable)" -D"KBUILD_MODNAME=KBUILD_STR(pgtable)" -c -o arch/x86/mm/.tmp_pgtable.o arch/x86/mm/pgtable.c'

parser = Lark(grammar, start='singleCmd')
tree = parser.parse(input_string)
print(tree.pretty())