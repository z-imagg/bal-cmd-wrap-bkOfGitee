#!/usr/bin/python3

#apt install file uuid-runtime

import sys
import time
import subprocess
from typing import List

#参数数组复制一份，不要直接修改sys.argv
Argv=list(sys.argv)

# 打印参数
_ArgvStr:str=' '.join(Argv)
print( f"收到clang参数: {_ArgvStr}" )


#-Werror 警告视为错误
#-Wno-error 禁止将警告视为错误
#-Wno-error -Werror : 依次执行 即 ： 先禁止后允许 结果是 允许

 #如果参数中含有-Werror , 将其替换为 -Wno-error. 
Argv:List[str] = ["" if argK == "-Werror" else argK   for argK in Argv]

#后缀
SUFFIX="origin"

#clang的bin目录
CLANG_HOME_BIN:str="/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/bin"

"""

clang的c、c++编译器软链接关系：
clang++【软链接】 ----> clang【软链接】 ---->  clang-15【真ELF可执行文件】
真正的ELF可执行文件 clang-15 内部通过 当前命令行程序名 是 clang 还是 clang++ 以获知当前应该做c编译 还是 做c++编译

可见 :
1. 以上 "clang的c、c++编译器软链接关系" 不能被破坏，否则肯定不能正常工作

可见，错误的包装器:
2. 包装器  如果   穿插 到 "clang的c、c++编译器软链接关系" 内部，则一定出错
    但假若  包装器 直接替代 "clang++【软链接】"、 "clang【软链接】"  ，有可能能正常工作 但这依赖于  "真正的ELF可执行文件 clang-15" 的内部实现，
       因此这不是好办法。

可见，正确的包装器:
3. 包装器  如果   凌驾于  "clang的c、c++编译器软链接关系" 之上，则一定能正常工作

此处使用的包装器:
clang++.wrap.py【软链接】 ---->  clang-15.wrap.py【py脚本包装器】  ----调用----> clang++【软链接】
clang.wrap.py  【软链接】 ---->  clang-15.wrap.py【py脚本包装器】  ----调用----> clang【软链接】
以上文件都在目录 CLANG_HOME_BIN 中。
其中 "clang-15.wrap.py【py脚本包装器】" 通过 当前命令行程序名 来判断 应该调用 "clang++【软链接】" 、"clang【软链接】" 中的哪一个.

##### "clang的c、c++编译器软链接关系" 如下:
cd /llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/bin
ls -lhrt clang*
-rwxr-xr-x  169M  1月 18  2023 clang-15
lrwxrwxrwx  5     1月 18  2023 clang++ -> clang
lrwxrwxrwx  8     1月 18  2023 clang -> clang-15

#### "真正的ELF可执行文件 clang-15 内部通过 当前命令行程序名 是 clang 还是 clang++ 以获知当前应该做c编译 还是 做c++编译"  如何知道这一点的？
以下结构，在编译最简单的c++程序src.cxx时 链接报错  , 这说明 "真正的ELF可执行文件 clang-15" 此时 以为是要编译c语言  ，所以才会链接这样报错 
clang++【软链接】 ---->  clang-15.wrap.py【py脚本包装器】  ----> 真正的ELF可执行文件 clang-15
clang  【软链接】 ---->  clang-15.wrap.py【py脚本包装器】  ----> 真正的ELF可执行文件 clang-15
链接报错信息如下:
'''
cat clang-15-1691989413275951104.stderr
/usr/bin/ld: CMakeFiles/cmTC_b6d5e.dir/src.cxx.o: in function `main':
src.cxx:(.text+0x4e): undefined reference to `std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >::~basic_string()'
/usr/bin/ld: CMakeFiles/cmTC_b6d5e.dir/src.cxx.o: in function `std::__cxx11::to_string(int)':
src.cxx:(.text._ZNSt7__cxx119to_stringEi[_ZNSt7__cxx119to_stringEi]+0x7a): undefined reference to `std::allocator<char>::allocator()'
/usr/bin/ld: src.cxx:(.text._ZNSt7__cxx119to_stringEi[_ZNSt7__cxx119to_stringEi]+0x90): undefined reference to `std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >::basic_string(unsigned long, char, std::allocator<char> const&)'
/usr/bin/ld: src.cxx:(.text._ZNSt7__cxx119to_stringEi[_ZNSt7__cxx119to_stringEi]+0x9e): undefined reference to `std::allocator<char>::~allocator()'
/usr/bin/ld: src.cxx:(.text._ZNSt7__cxx119to_stringEi[_ZNSt7__cxx119to_stringEi]+0xb0): undefined reference to `std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >::operator[](unsigned long)'
/usr/bin/ld: src.cxx:(.text._ZNSt7__cxx119to_stringEi[_ZNSt7__cxx119to_stringEi]+0xf0): undefined reference to `std::allocator<char>::~allocator()'
/usr/bin/ld: src.cxx:(.text._ZNSt7__cxx119to_stringEi[_ZNSt7__cxx119to_stringEi]+0x10a): undefined reference to `std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >::~basic_string()'
/usr/bin/ld: src.cxx:(.text._ZNSt7__cxx119to_stringEi[_ZNSt7__cxx119to_stringEi]+0x118): undefined reference to `std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >::~basic_string()'
/usr/bin/ld: CMakeFiles/cmTC_b6d5e.dir/src.cxx.o:(.data.DW.ref.__gxx_personality_v0[DW.ref.__gxx_personality_v0]+0x0): undefined reference to `__gxx_personality_v0'
clang-15: error: linker command failed with exit code 1 (use -v to see invocation)
'''
"""
#原始命令.
# 其中 "clang-15.wrap.py【py脚本包装器】" 通过 当前命令行程序名 来判断 应该调用 "clang++【软链接】" 、"clang【软链接】" 中的哪一个.
# ProgramNameInCmd=sys.argv[0]
ProgramNameInCmd=Argv[0]
WRAP_PY_SUFFIX=".wrap.py"
orginCmd:str=ProgramNameInCmd.replace(WRAP_PY_SUFFIX,"")
#此时 orginCmd 为   "clang【软链接】: {CLANG_HOME_BIN}/clang"  或 "clang++【软链接】 : {CLANG_HOME_BIN}/clang++"  ,

#替换可执行文件路径为原始clang-15路径
Argv[0]=orginCmd

#clang命令输出文件路径，文件名尽可能唯一
current_sec = int(time.time())  # 获取当前的绝对秒数
current_ns = time.perf_counter_ns()  # 获取当前的纳秒数
CurrNanoSeconds = int(current_sec * 1e9 + current_ns)  # 合成当前的绝对时刻（以纳秒为单位）

OF_cmd:str=f"/tmp/clang-15-{CurrNanoSeconds}.cmd"
OF_stdout:str=f"/tmp/clang-15-{CurrNanoSeconds}.stdout"
OF_stderr:str=f"/tmp/clang-15-{CurrNanoSeconds}.stderr"

exitCode:int=None
with open(OF_cmd, "w") as ofCmd:
    # 调用clang15命令，并将正常输出、错误输出写入文件
    ArgvStr:str=' '.join(Argv)
    #命令写入文件，方便问题查找.
    ofCmd.write(f"实际执行clang命令:{ArgvStr}\n")
    with open(OF_stdout, "w") as of_stdout:
        with open(OF_stderr, "w") as of_stderr:
            #subprocess.run ：
            #   直接用数组 Argv， 不要用字符串样式的ArgvStr
            #     shell=False  或  无 shell=True， 则第一个参数Argv必须是列表 而不能是一个长字符串
            print("实际执行clang命令:",Argv)
            process_R=subprocess.run(Argv,  stdout=of_stdout, stderr=of_stderr,text=True)
            exitCode=process_R.returncode

assert exitCode is not None
print(f"退出代码:{exitCode}")

with open(OF_stdout, "r") as if_stdout:
    stdout:str=if_stdout.read()
    print(f"标准输出:{stdout}")
with open(OF_stderr, "r") as if_stderr:
    stderr:str=if_stderr.read()
    if stderr is not None and len(stderr.strip()) >0 :
        print(f"标准错误输出:{stderr}")

# 检查命令执行结果
if exitCode != 0:
    # 命令执行报错，检查错误信息
    with open(OF_stderr, "r") as of_stderr:
        error_message=of_stderr.read()
        # input("编译出错，暂时停在这里")
        exit(exitCode)

        # # 检查错误信息中是否包含特定的undefined reference错误
        # if [[ $error_message =~ "undefined reference to X__t_clock_tick" ]] ||
        #    [[ $error_message =~ "undefined reference to X__funcEnter" ]] ||
        #    [[ $error_message =~ "undefined reference to X__funcReturn" ]]; then
        #     echo "Adding $tick_obj to arguments and running ld again"
        # 	/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/bin/clang++ -c /pubx/pytorch/t_clock_tick/t_clock_tick.cpp -o $tick_obj
        #     $orginLd "$@" $tick_obj
        # fi

