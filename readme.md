
举例  使用 本编译器拦截器  编译pytorch-v1.0.0 ， http://giteaz:3000/wiki/github-gitee-GITEA/src/commit/935b9ddbc3674c4375e7c7af983b05536261464c/torch-v1.0.0-build.md




#### 修改ninja的py包裹脚本，使得显示编译命令
```shell


/fridaAnlzAp/cmd-wrap/.venv/lib/python3.10/site-packages/ninja/data/bin/ninja --help
# -v, --verbose  show all command lines while building


```



```python
#/fridaAnlzAp/cmd-wrap/.venv/bin/ninja
if __name__ == '__main__':
    if len(sys.argv)>=1: sys.argv.insert(1,"--verbose") #增加此行, 即可使得ninja在编译时显示所用编译命令
    #...
```