
```base_ubuntu_22.04.04:0.1 ``` 来自 http://giteaz:3000/frida_analyze_app_src/main/src/branch/fridaAnlzAp/docker/docker/main_dockerImage_build_run.sh

```shell
docker run --privileged=true  --name u22  -itd base_ubuntu_22.04.04:0.1 

```

http://giteaz:3000/bal/bal/src/branch/bal/dev/bldLinux4RunOnBochs/bochs2.7boot-syslinux-linux4.15.y.sh


```shell
git clone  -b bal/dev   http://giteaz:3000/bal/bal.git /
cd /bal
git submodule    update --recursive --init

apt install -y xxd
bash -x  bochs2.7boot-syslinux-linux4.15.y.sh

```