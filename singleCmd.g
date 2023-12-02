//cookie.g : copy from http://lab.antlr.org/  select cookies
//1.config jdk11
//2. vscode install antrl4 plugin
//3. vscode open cookie.g, show to run:
//    java -jar /home/z/.vscode/extensions/mike-lischke.vscode-antlr4-2.4.3/node_modules/antlr4ng-cli/antlr4-4.13.2-SNAPSHOT-complete.jar -message-format antlr -o /crk/clang-wrap/.antlr -listener -no-visitor -Xexact-output-dir /crk/clang-wrap/cookie.g




/*
本文法 在  http://lab.antlr.org/ 上 ，通过以下测试用例：

gcc   -D'KBUILD_STR(s)=#s' -D"KBUILD_BASENAME=KBUILD_STR(pgtable)" -D"KBUILD_MODNAME=KBUILD_STR(pgtable)" -c -o arch/x86/mm/.tmp_pgtable.o arch/x86/mm/pgtable.c

gcc -Wp,-MD,arch/x86/mm/.pgtable.o.d  -nostdinc -isystem /usr/lib/gcc/i686-linux-gnu/4.4.7/include -D__KERNEL__ -Iinclude  -I/crk/bochs/linux2.6-run_at_bochs/linux-2.6.27.15/arch/x86/include -include include/linux/autoconf.h -Wall -Wundef -Wstrict-prototypes -Wno-trigraphs -fno-strict-aliasing -fno-common -Werror-implicit-function-declaration -O2 -m32 -msoft-float -mregparm=3 -freg-struct-return -mpreferred-stack-boundary=2 -march=i686 -mtune=generic -ffreestanding -pipe -Wno-sign-compare -fno-asynchronous-unwind-tables -mno-sse -mno-mmx -mno-sse2 -mno-3dnow -Iinclude/asm-x86/mach-default -Wframe-larger-than=1024 -fno-stack-protector -fno-omit-frame-pointer -fno-optimize-sibling-calls -g -pg -Wdeclaration-after-statement -Wno-pointer-sign  -D"KBUILD_STR(s)=#s" -D"KBUILD_BASENAME=KBUILD_STR(pgtable)" -D"KBUILD_MODNAME=KBUILD_STR(pgtable)" -c -o arch/x86/mm/.tmp_pgtable.o arch/x86/mm/pgtable.c
 

 
 */

grammar singleCmd;

singleCmd
    : program (' ')+ av_pairs* (';')? EOF
    ;

program
    : TOKEN
    ;

av_pairs
    : av_pair ((' ')+ av_pair)*
    ;

av_pair
    : arg ('=' value)?
    | arg QUOTED_STRING
    ;

arg
    : TOKEN
    ;

value
    : word
    ;

word
    : TOKEN
    | QUOTED_STRING
    ;

//QUOTED_STRING 终结符不能用小写
QUOTED_STRING
    : '"' (~ ('"' | '\n'))* '"'
    | '\'' (~ ('\'' | '\n'))* '\''
    ;

TOKEN
    : ( '.' | '0' .. '9' | 'a' .. 'z' | 'A' .. 'Z' | '-'  | '/' | '_' | ':' | ',')+
    ;

DIGIT
    : '0' .. '9'
    ;

WS
    : [\t\r\n] -> skip
    ;