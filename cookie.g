//cookie.g : copy from http://lab.antlr.org/  select cookies
//1.config jdk11
//2. vscode install antrl4 plugin
//3. vscode open cookie.g, show to run:
//    java -jar /home/z/.vscode/extensions/mike-lischke.vscode-antlr4-2.4.3/node_modules/antlr4ng-cli/antlr4-4.13.2-SNAPSHOT-complete.jar -message-format antlr -o /crk/clang-wrap/.antlr -listener -no-visitor -Xexact-output-dir /crk/clang-wrap/cookie.g

grammar cookie;

cookie
    : av_pairs* EOF
    ;

name
    : attr
    ;

av_pairs
    : av_pair (';' av_pair)*
    ;

av_pair
    : attr ('=' value)?
    ;

attr
    : token
    ;

value
    : word
    ;

word
    : token
    | quoted_string
    ;

token
    : TOKEN
    ;

quoted_string
    : STRING
    ;

STRING
    : '"' (~ ('"' | '\n'))* '"'
    ;

TOKEN
    : ('0' .. '9' | 'a' .. 'z' | 'A' .. 'Z' | '-' | ' ' | '/' | '_' | ':' | ',')+
    ;

DIGIT
    : '0' .. '9'
    ;

WS
    : [\t\r\n] -> skip
    ;