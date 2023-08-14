
# clang的c、c++编译器软链接关系：
> clang++【软链接】 ----> clang【软链接】 ---->  clang-15【真ELF可执行文件】

> 真正的ELF可执行文件 clang-15 内部通过 当前命令行程序名 是 clang 还是 clang++ 以获知当前应该做c编译 还是 做c++编译

# 推论
>可见 :

1. 以上 "clang的c、c++编译器软链接关系" 不能被破坏，否则肯定不能正常工作

> 可见，错误的包装器:

2. 包装器  如果   穿插 到 "clang的c、c++编译器软链接关系" 内部，则一定出错
>    但假若  包装器 直接替代 "clang++【软链接】"、 "clang【软链接】"  ，有可能能正常工作 但这依赖于  "真正的ELF可执行文件 clang-15" 的内部实现，
>       因此这不是好办法。

> 可见，正确的包装器:
3. 包装器  如果   凌驾于  "clang的c、c++编译器软链接关系" 之上，则一定能正常工作

# 包装器结构
> 此处使用的包装器:
> clang++.wrap.py【软链接】 ---->  clang-15.wrap.py【py脚本包装器】  ----调用----> clang++【软链接】

> clang.wrap.py  【软链接】 ---->  clang-15.wrap.py【py脚本包装器】  ----调用----> clang【软链接】

> 以上文件都在目录 CLANG_HOME_BIN 中。

> 其中 "clang-15.wrap.py【py脚本包装器】" 通过 当前命令行程序名 来判断 应该调用 "clang++【软链接】" 、"clang【软链接】" 中的哪一个.

# 背景
## "clang的c、c++编译器软链接关系" 如下:
```bash
cd /llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/bin
ls -lhrt clang*
#-rwxr-xr-x  169M  1月 18  2023 clang-15
#lrwxrwxrwx  5     1月 18  2023 clang++ -> clang
#lrwxrwxrwx  8     1月 18  2023 clang -> clang-15
```

## 如何知道 clang-15 通过 命令行程序名 来确定做C或做C++ ?
>    "真正的ELF可执行文件 clang-15 内部通过 当前命令行程序名 是 clang 还是 clang++ 以获知当前应该做c编译 还是 做c++编译"  ， 如何知道这一点的?

> 以下结构，在编译最简单的c++程序src.cxx时 链接报错  , 这说明 "真正的ELF可执行文件 clang-15" 此时 以为是要编译c语言  ，所以才会链接报错如下面 

> clang++【软链接】 ---->  clang-15.wrap.py【py脚本包装器】  ----> 真正的ELF可执行文件 clang-15
> clang  【软链接】 ---->  clang-15.wrap.py【py脚本包装器】  ----> 真正的ELF可执行文件 clang-15

> 链接报错信息如下:
```bash
cat clang-15-1691989413275951104.stderr
'''
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
```