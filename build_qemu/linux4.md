
http://giteaz:3000/bal/bal/src/branch/bal/dev/bldLinux4RunOnBochs/bochs2.7boot-syslinux-linux4.15.y.sh

```shell
git clone  -b bal/dev   http://giteaz:3000/bal/bal.git /
cd /bal
git submodule    update --recursive --init

apt install -y xxd
bash -x  bochs2.7boot-syslinux-linux4.15.y.sh

```