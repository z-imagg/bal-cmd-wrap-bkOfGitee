
举例  使用 本编译器拦截器  编译pytorch-v1.0.0 ， http://giteaz:3000/wiki/github-gitee-GITEA/src/commit/935b9ddbc3674c4375e7c7af983b05536261464c/torch-v1.0.0-build.md


#### 建议docker下使用，否则可能破坏宿主机编译环境
```shell
sudo docker pull ubuntu:22.04

docker run --interactive --tty --detach   -v /fridaAnlzAp/:/fridaAnlzAp/ --name u22   ubuntu:22.04
docker exec -it u22  bash

#或者一步到shell:
#docker run --interactive --tty --detach   -v /fridaAnlzAp/:/fridaAnlzAp/ --name u22   ubuntu:22.04

docker stop u22
docker rm u22
```

#### 修改ninja的py包裹脚本，使得显示编译命令
```shell


/app/cmd-wrap/.venv/lib/python3.10/site-packages/ninja/data/bin/ninja --help
# -v, --verbose  show all command lines while building


```



```python
#/app/cmd-wrap/.venv/bin/ninja
if __name__ == '__main__':
    if len(sys.argv)>=1: sys.argv.insert(1,"--verbose") #增加此行, 即可使得ninja在编译时显示所用编译命令
    #...
```


####  根据入口者查询业务者


http://giteaz:3000/bal/cmd-wrap/src/tag/v2.1.simpl/tool_bin/readme.md