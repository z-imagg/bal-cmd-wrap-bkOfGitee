#### 编译testdisk


####  docker下使用，否则可能破坏宿主机编译环境
```shell
sudo docker pull ubuntu:22.04

LLVM_15=/app/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/
docker run --interactive --tty --detach -v $LLVM_15:$LLVM_15 -v /app/cmd-wrap/:/app/cmd-wrap/  -v /fridaAnlzAp/:/fridaAnlzAp/ --name u22   ubuntu:22.04
docker exec -it u22  bash

#或者一步到shell:
#docker run --interactive --tty --detach   -v /fridaAnlzAp/:/fridaAnlzAp/ --name u22   ubuntu:22.04

# docker stop u22
# docker rm u22
```

```shell
apt update
apt install -y build-essential
apt install -y file sudo
apt install -y python3.10 python3.10-venv
ln -s /usr/bin/python3 /usr/bin/python
```


```shell
cd /fridaAnlzAp/
git clone https://gitee.com/disk_recovery/cgsecurity--testdisk.git
#切换到 git分支 fridaAnlzAp/main
# git submodule update --init --progress --recursive 

```

基于提交   https://gitee.com/disk_recovery/cgsecurity--testdisk/commit/43f9e24596cafa34241384dad191c1ac7ad47cec

##### 2. 编译器的拦截器（可选）（对分析业务来说是必须的）

基于拦截器版本， http://giteaz:3000/bal/cmd-wrap/commit/3cdb3ddb6e30803cbe1ca105d85453190e61b4be

```shell

#建立python虚拟环境 /app/cmd-wrap/.venv/
bash /app/cmd-wrap/script/env_prepare.sh

#编写 原始命令、入口命令
bash -x /app/cmd-wrap/script/cmd_setup.sh

which c++ #/usr/bin/c++

readlink -f $(which c++) #/app/cmd-wrap/bin/interceptor_xx.py

which python #/app/cmd-wrap/.venv/bin/python

python --version #Python 3.10.12

```

#####  3. 编译正文
```shell
cd /fridaAnlzAp/cgsecurity--testdisk/

apt install -y autoconf automake
apt install -y libncurses5-dev 
#apt install apt-file
#apt-file update
#apt-file search pkg-config
apt install -y pkg-config

# testdisk已经禁止了qt ，不再需要安装qt
# apt install -y qtbase5-dev-tools qtbase5-dev libpolkit-qt5-1-* libqt53dcore5

source /app/cmd-wrap/.venv/bin/activate
source /app/cmd-wrap/script/pythonpath.sh
env | grep PYTHONPATH

rm -frv /tmp/*

#以下4行是原始编译步骤
make clean ; 
rm -fr config ;  
bash autogen.sh ;
bash compile.sh ;
#注意表明看 编译选项 还是 '-O2 -g' ， 但实际上 拦截器已经将 其替换为 '-O1 -g1'了

#cmd-wrap有时不会逐步输出日志，所以 看起来像死了一样，其实没死， 等到全部编译完成了 会有日志输出

#cmd-wrap的日志都在/tmp/下
ls -lh /tmp/*.log | wc  -l 
# 506

grep --text  "\-O1" /tmp/*.log   | wc -l 
# 503

grep --text  "\-g1" /tmp/*.log   | wc -l 
# 503


#撤销拦截器
bash /app/cmd-wrap/script/remove_interceptor.sh
deactivate
```

##### 4. 编译产物

不加c++编译器拦截器时 编译出的 testdisk 尺寸是 1.7M，  用c++编译器拦截器将-g改为-g1、将-O2改为-O1 编译出的 testdisk 尺寸是 602K 

具体如下：


###### 若 不使用 "2. 编译器的拦截器（可选）"，
即 不加c++编译器拦截器时 编译出的 testdisk 尺寸是 1.7M

编译结果 
```shell
file ./src/testdisk ./src/photorec
# ./src/testdisk: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=b46df95797a48cbc4305322332ae113b018d4cc4, for GNU/Linux 3.2.0, with debug_info, not stripped
# ./src/photorec: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=14e06a604e5b1283565065f32ef8cf3d452f46b1, for GNU/Linux 3.2.0, with debug_info, not stripped

ls -lh  ./src/testdisk ./src/photorec
# -rwxrwxr-x 1 z z 3.4M  4月  8 13:25 ./src/photorec
# -rwxrwxr-x 1 z z 1.7M  4月  8 13:25 ./src/testdisk


```

######  若 使用了 "2. 编译器的拦截器（可选）"，
即 用c++编译器拦截器将-g改为-g1、将-O2改为-O1 编译出的 testdisk 尺寸是 602K 

编译结果, 
```shell
file ./src/testdisk ./src/photorec
# ./src/testdisk: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=f207f570f122a860028627dfcebaca34aa036c84, for GNU/Linux 3.2.0, with debug_info, not stripped
# ./src/photorec: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=c54a912514fe8b178bdedb7fa5383dfe06fd4ca4, for GNU/Linux 3.2.0, with debug_info, not stripped


ls -lh  ./src/testdisk ./src/photorec
# -rwxrwxrwx 1 1000 1000 1.2M Apr  8 07:39 ./src/photorec
# -rwxrwxrwx 1 1000 1000 602K Apr  8 07:39 ./src/testdisk



```


#### 使用testdisk

此时回到宿主机, docker 实例 和 宿主机 操作系统 都是 ubuntu 22.04


##### 制作磁盘映像文件
```shell
sudo apt install -y syslinux syslinux-common syslinux-efi syslinux-utils

rm -fr hd.img hd_mnt/
mkdir hd_mnt/

#制作磁盘映像文件，返回分区的第一个字节下标
#                                                 CHS参数
#               mkdiskimage  -F  -o   $HdImgF $HdImg_C $HdImg_H $HdImg_S 
Part1stByteIdx=$(mkdiskimage  -F  -o   hd.img   5        255        63)
#这里 Part1stByteIdx == 16384

#不要乱用CHS参数，否则testdisk认不出来


#mount形成链条:  $HdImgF --> /dev/loopX --> $hd_img_dir/
sudo mount --verbose --options loop,offset=$Part1stByteIdx hd.img ./hd_mnt 
loopX=$(sudo losetup   --raw   --associated hd.img  | cut -d: -f1)
# loopX == /dev/loop12
lsblk $loopX 
# NAME   MAJ:MIN RM SIZE RO TYPE MOUNTPOINTS
# loop12   7:12   0   5M  0 loop /fridaAnlzAp/cgsecurity--testdisk/hd_mnt

echo aaabbbcccddeff1200000 | sudo tee   hd_mnt/test.txt
echo ===================== | sudo tee   hd_mnt/log.txt
sudo rm -frv hd_mnt/*

#卸载:
sudo losetup --detach $loopX
sudo umount hd.img; sudo umount ./hd_mnt

```

```shell

ls -lh hd.img 
# -rwxrwxrwx 1 z z 1.3M  4月  8 16:13 hd.img

fdisk -l  hd.img 
# Disk hd.img: 1.25 MiB, 1310720 bytes, 2560 sectors
# Units: sectors of 1 * 512 = 512 bytes
# Sector size (logical/physical): 512 bytes / 512 bytes
# I/O size (minimum/optimal): 512 bytes / 512 bytes
# Disklabel type: dos
# Disk identifier: 0x876401f5

# Device     Boot Start   End Sectors  Size Id Type
# hd.img1    *       32  2559    2528  1.2M  1 FAT12

```

##### 将磁盘映像文件hd.img喂给testdisk
```shell
#列出分区
./src/testdisk /list   hd.img 
```

###### testdisk恢复已删除文件步骤举例



```shell
./src/testdisk    hd.img 
#操作步骤:
# Processed
# Intel
# Geometry ， 检查 CHS是否匹配
# Analyze
#  'Quick Search'
#   按回车'Continue'
#   'Deeper Search'
#    按'P' 即'list files'  ， 此时 列出了两个刚刚删除的文件 test.txt 、log.txt
```


###### gdb观看__loop_step__执行次数



###### gdb脚本
```shell

echo '''
set logging file __loop_step__.gdb.log
set logging enabled on
set print pretty on
set pagination off
set breakpoint pending on

break ___loop_step__
commands 1
 #backtrace
 #frame 1
 #info locals
 continue
end

run
quit
''' > ./__loop_step__.gdb_script 

```


###### gdb执行testdisk

testdisk执行步骤 参考上一步  'testdisk恢复已删除文件步骤举例'

```shell

rm -fr  __loop_step__.gdb.log 
gdb -q  --command ./__loop_step__.gdb_script --args  ./src/testdisk    hd.img 
grep "Breakpoint 1" __loop_step__.gdb.log |  wc -l  
#9  #即 调用函数__loop_step__次数为9

```

