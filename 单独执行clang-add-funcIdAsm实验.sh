#此时在ubuntu2264下
cd /ubt14x86root/crk/bochs/linux2.6-run_at_bochs/linux-2.6.27.15


#原始命令是 :
# gcc -Wp,-MD,arch/x86/kernel/.i8259.o.d  -nostdinc -isystem /usr/lib/gcc/i686-linux-gnu/4.4.7/include -D__KERNEL__ -Iinclude  -I/crk/bochs/linux2.6-run_at_bochs/linux-2.6.27.15/arch/x86/include -include include/linux/autoconf.h -Wall -Wundef -Wstrict-prototypes -Wno-trigraphs -fno-strict-aliasing -fno-common -Werror-implicit-function-declaration -O2 -m32 -msoft-float -mregparm=3 -freg-struct-return -mpreferred-stack-boundary=2 -march=i686 -mtune=generic -ffreestanding -pipe -Wno-sign-compare -fno-asynchronous-unwind-tables -mno-sse -mno-mmx -mno-sse2 -mno-3dnow -Iinclude/asm-x86/mach-default -Wframe-larger-than=1024 -fno-stack-protector -fno-omit-frame-pointer -fno-optimize-sibling-calls -g -pg -Wdeclaration-after-statement -Wno-pointer-sign  -D"KBUILD_STR(s)=#s" -D"KBUILD_BASENAME=KBUILD_STR(i8259)"  -D"KBUILD_MODNAME=KBUILD_STR(i8259)" -c -o arch/x86/kernel/.tmp_i8259.o arch/x86/kernel/i8259.c


#直接改造为:
/app/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/bin/clang++  -Xclang   -load -Xclang  /crk/clang-add-funcIdAsm/build/lib/libCTk.so  -Xclang   -add-plugin -Xclang  CTk     -isystem /ubt14x86root/usr/lib/gcc/i686-linux-gnu/4.4.7/include   -Iinclude  -I/ubt14x86root/crk/bochs/linux2.6-run_at_bochs/linux-2.6.27.15/arch/x86/include -include include/linux/autoconf.h   -Iinclude/asm-x86/mach-default   -c  arch/x86/kernel/i8259.c

#   （由于 clang插件只是语法层面的，因此 上述 命令中  后端部分参数    -m32   -march=i686     可以丢弃）

#会报错:
#  include/linux/ioport.h:122:15: error: unknown type name 'resource_size_t'; did you mean 'resource_list'?

# { 开始 尝试解决报错
#在 ubuntu14x64下执行以下命令:
find / -name "*include*" -a -type d | tee inc.d.txt
cat inc.d.txt | xargs -I% find %  -type f   | tee headerf.txt
cat headerf.txt | xargs -I%   sh -c "grep -Hn    resource_size_t    %  | grep typedef"
#/usr/src/linux-headers-4.4.0-142/include/linux/types.h:167:typedef phys_addr_t resource_size_t;

#由此可见  上述命令需要增加 -I/ubt14x86root/usr/src/linux-headers-4.4.0-142/include/linux
# 结束 尝试解决报错}


/app/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/bin/clang++  -Xclang   -load -Xclang  /crk/clang-add-funcIdAsm/build/lib/libCTk.so  -Xclang   -add-plugin -Xclang  CTk  -I/ubt14x86root/usr/src/linux-headers-4.4.0-142/include/linux   -isystem /ubt14x86root/usr/lib/gcc/i686-linux-gnu/4.4.7/include   -Iinclude  -I/ubt14x86root/crk/bochs/linux2.6-run_at_bochs/linux-2.6.27.15/arch/x86/include -include include/linux/autoconf.h   -Iinclude/asm-x86/mach-default   -c  arch/x86/kernel/i8259.c

# 此时有更多的报错
#  include/asm/bitops.h:116:2: error: use of undeclared identifier 'barrier'
#  include/asm/bitops.h:61:13: error: use of undeclared identifier 'u8'

#结论:   想要抄 低版本 linux内核源码 的编译命令 给 clang15插件 执行，会有大量报错，  原因像是 因为 版本 差别 太大？   所以可以能 编译高版本内核？