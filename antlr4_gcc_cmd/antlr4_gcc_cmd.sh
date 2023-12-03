/app/miniconda3/bin/activate
pip install antlr4-python3-runtime
pip install antlr4-tools

antlr4 -Dlanguage=Python3 -o parser_generated -package parser_generated  SingleCmdLexer.g4
antlr4 -Dlanguage=Python3 -o parser_generated -package parser_generated  SingleCmdParser.g4

#https://www.azul.com/downloads/?version=java-11-lts&package=jdk#zulu
#https://cdn.azul.com/zulu/bin/zulu11.68.17-ca-jdk11.0.21-linux_i686.tar.gz
