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

##### 2. 编译器的拦截器（可选）（对分析业务来说是必须的）

基于拦截器版本， http://giteaz:3000/bal/cmd-wrap/commit/3cdb3ddb6e30803cbe1ca105d85453190e61b4be

```shell

bash /app/cmd-wrap/script/env_prepare.sh
bash -x /app/cmd-wrap/script/cmd_setup.sh
#确保 最行末尾 是 '存' 而不是 '无'

which c++ #/usr/bin/c++

readlink -f $(which c++) #/app/cmd-wrap/bin/interceptor_cxx.py

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
apt install -y qtbase5-dev-tools qtbase5-dev libpolkit-qt5-1-* libqt53dcore5

rm -frv /tmp/*
make clean ; 
rm -fr config ;  
bash autogen.sh ;
bash compile.sh ;
#注意表明看 编译选项 还是 '-O2 -g' ， 但实际上 拦截器已经将 其替换为 '-O1 -g1'了

#cmd-wrap有时不会逐步输出日志，所以 看起来像死了一样，其实没死， 等到全部编译完成了 会有日志输出

#cmd-wrap的日志都在/tmp/下
ls -lh /tmp/*.log | wc  -l 
# 417

grep --text  "\-O1" /tmp/*.log   | wc -l 
# 414

grep --text  "\-g1" /tmp/*.log   | wc -l 
#414


#撤销拦截器
bash /app/cmd-wrap/script/remove_interceptor.sh
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
#./src/testdisk: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=09cac28ceaef70aa48f8d4030eb8d114dcbc0fee, for GNU/Linux 3.2.0, with debug_info, not stripped
#./src/photorec: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=52209b4c306a080cdd13707a8b98398a893f3c45, for GNU/Linux 3.2.0, with debug_info, not stripped

ls -lh  ./src/testdisk ./src/photorec
# -rwxrwxrwx 1 1000 1000 1.2M Apr  8 14:46 ./src/photorec
# -rwxrwxrwx 1 1000 1000 602K Apr  8 14:46 ./src/testdisk


```