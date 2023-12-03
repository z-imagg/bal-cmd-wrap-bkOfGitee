lexer grammar SingleCmdLexer;

SEP_EQ: '=';
SEP_SPC: ' ';
SEP_COMMA: ',';

STR: STR_ | STR_ESC;

TK_NORMAL: [^-][0-9a-zA-Z-_/.]*;

TK_ANY: (',' | '-' | SL | L | D)+;

SL: '_' | '/' | '.' | '=';

D: 	[0-9];
LL: [a-z];
//[a-zA-Z$_]
UL: [A-Z];
L: LL | UL;

STR_: STR_DQ_ | STR_SQ_;
DQ: '"';
SQ: '\'';
STR_INNER_: ~['\\\r\n];
// ~[\r\n]  表示匹配任何一个不是 \r 或 \n 的字符(非贪婪模式)
STR_DQ_: DQ STR_INNER_ DQ;
STR_SQ_: SQ STR_INNER_ SQ;

STR_ESC: STR_DQ_ESC_ | STR_SQ_ESC_;
STR_DQ_ESC_: DQ_ESC STR_INNER_ DQ_ESC;
STR_SQ_ESC_: SQ_ESC STR_INNER_ SQ_ESC;
DQ_ESC: '\\"';
SQ_ESC: '\\\'';

FILE_NAME: (FILE_NAME_LEAD | D | L) (FILE_NAME_MID | D | L)+;
FILE_NAME_LEAD: '.' | '_' | ',' | '+' | '/';
FILE_NAME_MID: FILE_NAME_LEAD | '-';

WS: [ \t]+ -> skip;



ARG_INC: '-I';
KEY: '-' ('-')? (L | D) (('_' | L | D)*);
