parser grammar SingleCmdParser;
options {
tokenVocab=SingleCmdLexer;
}

singleCmd: gcc_cmd;

gcc_cmd: gcc_cmd_1 | gcc_cmd_3;

gcc_cmd_1: program kv_ls* src_file;

gcc_cmd_3: program kv_ls* file+;

program: FILE_NAME;
src_file: FILE_NAME;
file: FILE_NAME;

kv_ls: kv+;

kv: kv3 | kv4 | kv5 | key | kv1 | kv2;

kv1: key SEP_SPC val_normal;
kv4: key SEP_EQ val_normal;
kv5: key STR;
kv2: key SEP_COMMA val_any;
kv3: arg_inc val_normal;

arg_inc: ARG_INC;
key: KEY;
val_normal: TK_NORMAL | STR;
val_any: TK_ANY | STR;


