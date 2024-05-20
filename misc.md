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


####  根据入口者查询目者


http://giteaz:3000/bal/cmd-wrap/src/tag/v2.1.simpl/tool_bin/readme.md