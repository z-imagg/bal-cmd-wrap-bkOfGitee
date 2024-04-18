
#### 在docker实例中编译qemu
http://g:3000/frida_analyze_app_src/main/src/branch/main/docker/base_ubuntu_22_Dockerfile

```shell
docker run -itd --name u22 --hostname u22_dk base_ubuntu_22.04:0.1
docker exec -it u22 bash
```
#### 依赖搜索记录
```shell
apt install apt-file
apt-file update
```
```shell
apt-file search --regexp  "/pkg-config$"
#pkg-config: /usr/bin/pkg-config

apt-file search --regexp  "/ninja$"
#ninja-build: /usr/bin/ninja               

```
#### 编译qemu
参考, https://hlyani.github.io/notes/openstack/qemu_make.html

```shell
apt install -y python3-venv python3-pip  ninja-build pkg-config libglib2.0-dev
# pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip config set global.index-url https://mirrors.ustc.edu.cn/pypi/web/simple


git clone -b v8.2.2 https://gitee.com/imagg/qemu--qemu.git /app/qemu
#file /app/qemu--qemu/.git/config

mkdir /app/qemu/build; cd /app/qemu/build;
#以下三行为编译步骤
../configure --target-list=i386-softmmu,x86_64-softmmu
make -j4
# make install

```

#### 编译产物

##### 产物
```shell
find /app/qemu/build/ -type f -executable -and \( ! -path '*/tests/*' \) -and  \( ! -path '*/pyvenv/*' \) -and \( ! -path '*/contrib/*'  \) | xargs -I@ ls -sh       @
#精确尺寸: '| xargs -I@ stat --format="%n %s"     @'
```

```txt
132K /app/qemu/build/subprojects/libvhost-user/link-test
14M /app/qemu/build/storage-daemon/qemu-storage-daemon
2.6M /app/qemu/build/qemu-edid
4.0K /app/qemu/build/config.status
70M /app/qemu/build/qemu-system-i386
11M /app/qemu/build/qemu-io
16K /app/qemu/build/meson-private/sanitycheckc.exe
11M /app/qemu/build/qemu-img
12M /app/qemu/build/qemu-nbd
2.6M /app/qemu/build/qemu-bridge-helper
3.7M /app/qemu/build/qga/qemu-ga
71M /app/qemu/build/qemu-system-x86_64
4.0M /app/qemu/build/qemu-pr-helper


```

##### qemu-system-i386 
1. 【描述】 ```file /app/qemu/build/qemu-system-i386  ```

```txt
        /app/qemu/build/qemu-system-i386: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=8e16b9741d22e249c55d6868fe63d301c535d7a1, for GNU/Linux 3.2.0, with debug_info, not stripped
```

2. 【依赖】 ```ldd /app/qemu/build/qemu-system-i386```
```txt
        linux-vdso.so.1 (0x00007ffd50af9000)
        libgio-2.0.so.0 => /lib/x86_64-linux-gnu/libgio-2.0.so.0 (0x00007a9f71f13000)
        libgobject-2.0.so.0 => /lib/x86_64-linux-gnu/libgobject-2.0.so.0 (0x00007a9f71eb3000)
        libglib-2.0.so.0 => /lib/x86_64-linux-gnu/libglib-2.0.so.0 (0x00007a9f71d79000)
        libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x00007a9f71d5d000)
        libgmodule-2.0.so.0 => /lib/x86_64-linux-gnu/libgmodule-2.0.so.0 (0x00007a9f71d56000)
        libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007a9f71c6f000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007a9f71a44000)
        libmount.so.1 => /lib/x86_64-linux-gnu/libmount.so.1 (0x00007a9f71a00000)
        libselinux.so.1 => /lib/x86_64-linux-gnu/libselinux.so.1 (0x00007a9f719d4000)
        libffi.so.8 => /lib/x86_64-linux-gnu/libffi.so.8 (0x00007a9f719c7000)
        libpcre.so.3 => /lib/x86_64-linux-gnu/libpcre.so.3 (0x00007a9f71951000)
        /lib64/ld-linux-x86-64.so.2 (0x00007a9f73818000)
        libblkid.so.1 => /lib/x86_64-linux-gnu/libblkid.so.1 (0x00007a9f71918000)
        libpcre2-8.so.0 => /lib/x86_64-linux-gnu/libpcre2-8.so.0 (0x00007a9f71881000)
```

##### qemu-system-x86_64 
1. 【描述】```file /app/qemu/build/qemu-system-x86_64```

```txt
        /app/qemu/build/qemu-system-x86_64: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=2aa26203fa5bdb52a2d0dfc020235ff9775ea910, for GNU/Linux 3.2.0, with debug_info, not stripped
```


2. 【依赖】 ```ldd /app/qemu/build/qemu-system-x86_64```
```txt
        linux-vdso.so.1 (0x00007ffcd77ec000)
        libgio-2.0.so.0 => /lib/x86_64-linux-gnu/libgio-2.0.so.0 (0x000073999a0d7000)
        libgobject-2.0.so.0 => /lib/x86_64-linux-gnu/libgobject-2.0.so.0 (0x000073999a077000)
        libglib-2.0.so.0 => /lib/x86_64-linux-gnu/libglib-2.0.so.0 (0x0000739999f3d000)
        libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x0000739999f21000)
        libgmodule-2.0.so.0 => /lib/x86_64-linux-gnu/libgmodule-2.0.so.0 (0x0000739999f1a000)
        libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x0000739999e33000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x0000739999c08000)
        libmount.so.1 => /lib/x86_64-linux-gnu/libmount.so.1 (0x0000739999bc4000)
        libselinux.so.1 => /lib/x86_64-linux-gnu/libselinux.so.1 (0x0000739999b98000)
        libffi.so.8 => /lib/x86_64-linux-gnu/libffi.so.8 (0x0000739999b8b000)
        libpcre.so.3 => /lib/x86_64-linux-gnu/libpcre.so.3 (0x0000739999b15000)
        /lib64/ld-linux-x86-64.so.2 (0x000073999b9e8000)
        libblkid.so.1 => /lib/x86_64-linux-gnu/libblkid.so.1 (0x0000739999adc000)
        libpcre2-8.so.0 => /lib/x86_64-linux-gnu/libpcre2-8.so.0 (0x0000739999a45000)
```

#### qemu翻译相关函数

#####  QEMU中被翻译的指令的生成和管理  的 源码文件和函数 （来自chatpgt-3.5-turbo）

1. **tcg.c**：
   - **`gen_intermediate_code()`**：这个函数负责生成目标代码的中间表示，作为进一步翻译的输入。
   - **`gen_intermediate_code_internal()`**：内部函数，用于生成目标代码的中间表示。

2. **translate-all.c**：
   - **`tb_gen_code()`**：这个函数负责生成翻译块（Translation Block）的代码，其中包括翻译后的指令。
   - **`gen_intermediate_code()`**：在一些版本中，这个函数也可能出现在`translate-all.c`文件中，负责生成目标代码的中间表示。

3. **tcg-runtime.c**：
   - **`tcg_gen_code()`**：这个函数负责生成TCG的代码，并将其加载到运行时环境中。
   - **`cpu_loop_exec()`**：在一些版本中，翻译后的指令的执行可能在这个函数中发生。

4. **exec.c**：
   - **`cpu_exec()`**：这个函数是QEMU的执行引擎，负责执行翻译后的指令。
   - **`tb_find()`**：用于查找指定的翻译块（Translation Block）。



#####  在 QEMU 8.2.2 版本中，QEMU中被翻译的指令的生成和管理  的 源码文件和函数 （来自chatpgt-3.5-turbo）

1. **translate-all.c 文件中的 translator_loop 函数**：在该函数中，QEMU 使用 Tiny Code Generator (TCG) 将客户机指令（例如 x86 指令）翻译成宿主机指令。翻译后的指令地址通常会在此处生成，并且可以追踪到该函数中的地址计算和指令生成过程。

2. **tcg/translate.c 文件中的 translate_insn 函数**：这个函数负责将单个指令翻译成宿主机指令。在该函数中，可以跟踪到翻译结果的生成过程，并且可以找到生成的宿主机指令的地址。

3. **exec.c 文件中的 cpu_exec_step 函数**：这个函数是 QEMU 中用于执行指令的核心函数之一。在这个函数中，可以找到虚拟机指令执行的主要逻辑，以及在执行过程中如何跳转到已经翻译后的指令地址。

4. **sysemu.c 文件中的 cpu_loop 函数**：在这个函数中，QEMU 主要是不断地执行客户机指令，同时会触发指令翻译的过程。在这个循环中，可以跟踪到翻译后的指令地址的使用和更新。


```shell
readelf --symbols ./qemu-system-x86_64 | egrep -w 'gen_intermediate_code|gen_intermediate_code_internal|tb_gen_code|gen_intermediate_code|tcg_gen_code|cpu_loop_exec|cpu_exec|tb_find'
```
```txt
 33430: 00000000008ba040 11442 FUNC    GLOBAL DEFAULT   16 tcg_gen_code
 34086: 00000000006d92a0  2214 FUNC    GLOBAL DEFAULT   16 tb_gen_code
 41116: 00000000006d2b00   975 FUNC    GLOBAL DEFAULT   16 cpu_exec
 49025: 000000000062dd40    82 FUNC    GLOBAL DEFAULT   16 gen_intermediate_code
```


```shell
readelf --symbols ./qemu-system-x86_64 | egrep -w 'translator_loop|translate_insn|cpu_exec_step|cpu_loop'
```

```txt
 40688: 00000000006d9f50  1118 FUNC    GLOBAL DEFAULT   16 translator_loop
```

#### qemu使用
```shell
/app/qemu/build/qemu-system-x86_64 --help
```


##### 放弃 linux-0.11


http://giteaz:3000/bal/cmd-wrap/src/branch/fridaAnlzAp/app/qemu/build_qemu/drop__linux-0.11.md

##### linux4

http://giteaz:3000/bal/cmd-wrap/src/branch/fridaAnlzAp/app/qemu/build_qemu/linux4.md