
#### 项目描述
本cmd-wrap项目的拦截器interceptor_xx.py理论上可以拦截任何命令， 

最初命令叫 interceptor_cxx.py 因为 只拦截 gcc、g++、c++、clang、clang++等编译命令，

现状是 interceptor_xx.py 可以拦截 编译命令 、make 、cmake， 但是 目前只配置了 拦截 编译命令

#### 存在的问题

#####  调用环
且 如果拦截 make 可以会形成自我调用的环， 没有仔细想有没有问题

拦截make形成的调用环： make ---> interceptor_xx.py  -->  make.origin --->  gcc --->  interceptor_xx.py  --> gcc.origin

很明显 interceptor_xx.py 以 进程的方式 自己调用自己了

#### 建议docker下使用，否则可能破坏宿主机编译环境

参考 [docker下使用，否则可能破坏宿主机编译环境](http://giteaz:3000/bal/cmd-wrap/src/branch/fridaAnlzAp/main/build_testdisk.md#docker%E4%B8%8B%E4%BD%BF%E7%94%A8%E5%90%A6%E5%88%99%E5%8F%AF%E8%83%BD%E7%A0%B4%E5%9D%8F%E5%AE%BF%E4%B8%BB%E6%9C%BA%E7%BC%96%E8%AF%91%E7%8E%AF%E5%A2%83)

#### cmd-wrap使用举例
##### 编译pytorch-v1.0.0

举例  使用 本编译器拦截器  编译pytorch-v1.0.0 ， http://giteaz:3000/wiki/github-gitee-GITEA/src/commit/935b9ddbc3674c4375e7c7af983b05536261464c/torch-v1.0.0-build.md

#####  cmd-wrap使用举例  ：  编译testdisk

举例  使用 本编译器拦截器  编译testdisk

http://giteaz:3000/bal/cmd-wrap/src/branch/fridaAnlzAp/main/build_testdisk.md





####  大杂烩
http://giteaz:3000/bal/cmd-wrap/src/branch/fridaAnlzAp/main/misc.md

