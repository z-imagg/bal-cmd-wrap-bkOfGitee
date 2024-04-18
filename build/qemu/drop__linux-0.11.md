
##### 放弃 linux-0.11


linux-0.11环境相关，https://gitee.com/repok/linux-0.11_yuan-xy__ctk/blob/tag/fridaAnlzAp/app/qemu/docker/build__linux_0.11__on__ubuntu_11.04.Dockerfile

必须使得qemu启动linux-0.11后， linux-0.11自主的关机， 即必须无交互性，这样frida或frida-trace才能正常使用

由于 不知道如何使linux0.11正常关机，  而 放弃 linux-0.11 了。

具体如下：

尝试修改其代码 让/bin/sh调用关机命令？ 但 貌似根本没有shutdown、halt、poweroff等命令，甚至根本不知道 其 工具集 是怎么来的？

从chatgpt-turbo-3.5得知 , linux 2.6之后才支持外部工具集 比如GNU工具集、BUSYBOX

由此可知 linux-0.11 可能很难 对接 后来的busybox工具集，  而且不确定busybox中是否有关机命令， 且 即使 对接上了 即使busybox有关机命令 还是不确定 是否能正常关闭linux0.11
