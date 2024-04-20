#!/usr/bin/env bash

# 【文件作用】 移除拦截器、恢复为原本真实的编译器、构建工具
# 不支持恢复到原样， 所以不要在物理机上使用cmd-wrap

sudo unlink /usr/bin/g++
sudo ln -s /usr/bin/x86_64-linux-gnu-g++-11 /usr/bin/g++

sudo unlink /usr/bin/cc
sudo ln -s /usr/bin/x86_64-linux-gnu-gcc-11 /usr/bin/cc

sudo unlink /usr/bin/c++
sudo ln -s /usr/bin/x86_64-linux-gnu-g++-11 /usr/bin/c++

sudo unlink /usr/bin/gcc
sudo ln -s /usr/bin/x86_64-linux-gnu-gcc-11 /usr/bin/gcc

# sudo unlink /usr/bin/cmake
#mv /usr/bin/cmake.origin /usr/bin/cmake

# sudo unlink /usr/bin/make
#mv /usr/bin/make.origin /usr/bin/make

sudo unlink /usr/bin/clang

sudo unlink /usr/bin/clang++




ls -lh /usr/bin/{gcc,g++,cc,c++,cmake,make}