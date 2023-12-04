from typing import List

#pip install paramiko

import paramiko
from paramiko import SSHClient
from lark_parser.file_at_cmd import FileAtCmd
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
    passwd_z = input("请输入主机ubuntu22x64的用户z的密码:")
    ubt22.connect('ubuntu22x64', port=2122, username='z', password=passwd_z)

    return ubt22

def clangAddFuncIdAsmWrap(fileAtGccCmd:FileAtCmd):
    #TODO : 调用远端主机ubuntu22x64上的clang-add-funcIdAsm插件修改本地ubuntu14x32上的源文件 , 源文件路径 及 头文件目录列表为 在 入参对象 fileAtCmd 中

    ubt22:SSHClient=__get_ubuntu22x64HostSshClient__()

    #  组装 clang 插件命令
    clang_plugin_so="/crk/clang-add-funcIdAsm/build/lib/libCTk.so"
    as_clang_cmd_part:str=fileAtGccCmd.__as_clang_cmd_part__()
    clang_plugin_cmd:str=f"/app/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/bin/clang  -Xclang   -load -Xclang {clang_plugin_so}  -Xclang   -add-plugin -Xclang  CTk   {as_clang_cmd_part}"
    #  clang 插件命令
    stdin, stdout, stderr = ubt22.exec_command(clang_plugin_cmd)

    # 获取命令输出
    output = stdout.read().decode('utf-8')

    # 打印输出结果
    print(output)

    # 关闭 SSH 连接
    ubt22.close()
