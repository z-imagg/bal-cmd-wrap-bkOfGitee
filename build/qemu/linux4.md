
```base_ubuntu_22.04.04:0.1 ``` 来自 http://giteaz:3000/frida_analyze_app_src/main/src/branch/fridaAnlzAp/docker/docker/main_dockerImage_build_run.sh

```shell
docker run -v /bal/:/bal/ -v /app/:/app/ --privileged=true  --name u22  -itd base_ubuntu_22.04.04:0.1 
docker exec -it u22 bash
```


##### 编译linux4
http://giteaz:3000/bal/bal/src/branch/bal/dev/bldLinux4RunOnBochs/bochs2.7boot-syslinux-linux4.15.y.sh


```shell
echo "10.0.4.9 giteaz" >> /etc/hosts


git clone  -b fridaAnlzAp/app/qemu-linux4   http://giteaz:3000/bal/bal.git /bal
cd /bal
git submodule    update --recursive --init

apt install -y xxd build-essential bc file cpio

cd /bal/bldLinux4RunOnBochs/

#编译 linux4
bash -x build-linux4.15.y-on-x64_u22.04.3LTS.sh
#制作 启动盘
bash -x  bochs2.7boot-syslinux-linux4.15.y.sh


```

##### 编译出的linux产物
```shell
ls -lh /bal/linux-stable/arch/x86/boot/bzImage  /bal/bldLinux4RunOnBochs/HD50MB200C16H32S.img 
# -rw-r--r-- 1 root root  50M Apr 18 14:36 /bal/bldLinux4RunOnBochs/HD50MB200C16H32S.img
# -rw-r--r-- 1 root root 6.2M Apr 18 14:30 /bal/linux-stable/arch/x86/boot/bzImage

```

##### qemu运行linux

######  自编译的qemu-system-x86_64 8.2.2 正常启动字符界面

```shell
/app/qemu/build-v8.2.2/qemu-system-x86_64 --version
#QEMU emulator version 8.2.2 (v8.2.2)


# 末尾加 '  -monitor stdio ' 可获得qemu控制台
/app/qemu/build-v8.2.2/qemu-system-x86_64 -nographic  -append "console=ttyS0"   /bal/bldLinux4RunOnBochs/HD50MB200C16H32S.img
#字符界面，正常启动到linux终端

/app/qemu/build-v8.2.2/qemu-system-x86_64 -nographic  -append "console=ttyS0"  -kernel  /bal/linux-stable/arch/x86/boot/bzImage -initrd /bal/bldLinux4RunOnBochs/initramfs-busybox-i686.cpio.tar.gz 
#字符界面，正常启动到linux终端

```

 


 
##### qemu下的linux4终端 正常关机 

```shell
/busybox-i686 ls /proc
#正常显示了各种进程id目录

/busybox-i686 ps auxf
#正常显示进程列表
```

```shell
/busybox-i686 poweroff -f 
#正常关机了
```