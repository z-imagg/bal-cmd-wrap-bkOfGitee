#!/usr/bin/env bash

# 【文件作用】 移除拦截器、恢复为原本真实的编译器、构建工具

sudo unlink /usr/bin/gcc
sudo cp -v --no-dereference /usr/bin/gcc.origin /usr/bin/gcc

sudo unlink /usr/bin/g++
sudo cp -v --no-dereference /usr/bin/g++.origin /usr/bin/g++

sudo unlink /usr/bin/c++
sudo cp -v --no-dereference /usr/bin/c++.origin /usr/bin/c++

sudo unlink /usr/bin/cmake
sudo cp -v --no-dereference /usr/bin/cmake.origin /usr/bin/cmake

sudo unlink /usr/bin/make
sudo cp -v --no-dereference /usr/bin/make.origin /usr/bin/make

ls -lh /usr/bin/{gcc,g++,c++,cmake,make}