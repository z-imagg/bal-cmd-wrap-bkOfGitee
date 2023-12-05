
#-1. rustup清华镜像使用参考
# https://mirrors.tuna.tsinghua.edu.cn/help/rustup/
echo 'export RUSTUP_UPDATE_ROOT=http://mirrors.tuna.tsinghua.edu.cn/rustup/rustup' >> ~/.bashrc
echo 'export RUSTUP_DIST_SERVER=http://mirrors.tuna.tsinghua.edu.cn/rustup' >> ~/.bashrc
source ~/.bashrc

#0.卸载旧版本 Rust（如果有）
rustup self uninstall

#1. 安装rustup
# 理论上只需要以下一条简单命令 ，即可
# curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
# 但由于国内下载国外慢, 所以改成:

wget --output-document ~/rustup-init.sh https://sh.rustup.rs
# 人工替换 rustup-init.sh 中的 大约93行
#    local _url="${RUSTUP_UPDATE_ROOT}/dist/${_arch}/rustup-init${_ext}"
# 为
#    local _url="http://mirrors.tuna.tsinghua.edu.cn/rustup/rustup/archive/1.26.0/i686-unknown-linux-gnu/rustup-init"
#                                 此处如果用过低版本的 rustup-init ，执行 rustup-init.sh 时 可能会报错 error: File too big rustc-1.74.0-i686-unknown-linux-gnu/rustc/lib/librustc_driver-66951ff08a396d2b.so

# 再执行
chmod +x ~/rustup-init.sh
~/rustup-init.sh
# 调试执行 :
#   sh -x    ~/rustup-init.sh


#2.设置环境变量
source ~/.cargo/env

#3.安装最新的 Rust
rustup update stable



