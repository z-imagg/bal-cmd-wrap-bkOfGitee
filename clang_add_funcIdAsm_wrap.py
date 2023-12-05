from typing import List

#pip install paramiko

from pathlib import Path
import paramiko
from paramiko import SSHClient
from lark_parser.file_at_cmd import FileAtCmd
def __readF__(filePath:str):
    with open(filePath,"r") as rf:
        text=rf.read()
        return text
    raise Exception(f"error __readF__ file:{filePath}")
def __writeF__(filePath:str,text:str)->bool:
    with open(filePath,"w") as wf:
        wf.write(text)
        return True
    raise Exception(f"error __readF__ file:{filePath}")
def __get_ubuntu22x64HostSshClient__()->SSHClient:
    # 创建 SSH 客户端
    ubt22:SSHClient = SSHClient()

    # 自动添加远程主机的密钥
    ubt22.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # 连接远程主机
    # F:\crk\bochs\linux2.6-run_at_bochs\readme.md
    """
# 各主机访问端口备忘
- win10Ssh: 192.168.1.13:3022; (__*)
- ubuntu14x32: 192.168.1.4:3022; (TPLINK_*)
- ubuntu22x64: 192.168.1.4:2122; (TPLINK_*)
    """
    passwd_z_f="/tmp/ubuntu22x64_z_pass.txt"
    if Path.exists(passwd_z_f):
        #下次使用已经保存的密码
        passwd_z=__readF__(passwd_z_f)
    else:
        #输入密码
        passwd_z = input("请输入主机ubuntu22x64的用户z的密码:")
        #保存密码
        __writeF__(passwd_z_f,passwd_z)
    ubt22.connect('ubuntu22x64', port=2122, username='z', password=passwd_z)

    return ubt22

def clangAddFuncIdAsmWrap(fileAtGccCmd:FileAtCmd):
    #TODO : 调用远端主机ubuntu22x64上的clang-add-funcIdAsm插件修改本地ubuntu14x32上的源文件 , 源文件路径 及 头文件目录列表为 在 入参对象 fileAtCmd 中

    ubt22:SSHClient=__get_ubuntu22x64HostSshClient__()

    """TODO
    在 ubuntu22上 将 ubuntu14的根目录 挂载 为 目录  /ubt14x86root, 在u22上执行以下命令:
    sudo apt-get update
    sudo apt-get install sshfs
    sudo sshfs -o allow_other,IdentityFile=/path/to/private_key z@ubuntu14x32:/ /ubt14x86root
    (以上三条命令是 以问题 “linux主机ubuntu14x32的根文件系统 挂载 到 主机ubuntu22x64的 目录 /u14root下 如何实施？” 问 https://vip.easychat.work/#/  得到的答复）
    """
    #  组装 clang 插件命令
    clang_plugin_so="/crk/clang-add-funcIdAsm/build/lib/libCTk.so"
    # as_clang_cmd_part 中 的目录 已经增加了前缀 /ubt14x86root
    as_clang_cmd_part:str=fileAtGccCmd.__as_clang_cmd_part__()
    clang_plugin_cmd:str=f"/app/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/bin/clang  -Xclang   -load -Xclang {clang_plugin_so}  -Xclang   -add-plugin -Xclang  CTk   {as_clang_cmd_part}"
    #  clang 插件命令
    stdin, stdout, stderr = ubt22.exec_command(clang_plugin_cmd)
    #理论上，clang插件已经对 源文件做出了 修改

    # 获取命令输出
    output = stdout.read().decode('utf-8')

    # 打印输出结果
    print(output)

    # 关闭 SSH 连接
    ubt22.close()
