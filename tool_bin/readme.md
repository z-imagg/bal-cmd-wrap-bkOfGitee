**根据入口者查询业务者**


###  使用说明

#### 安装py环境
去清华大学镜像安装某个版本的miniconda，比如 Miniconda3-py310_22.11.1-1

#### 在py环境中安装依赖

```shell
source /app/Miniconda3-py310_22.11.1-1/bin/activate
pip install -r /app/bash-simplify/bash-complete-gen-from-help/requirements.txt
```

#### 将此工具引入ubuntu22系统中(不影响系统自带python)


将以下这段代码 放入 ```~/.bash_profile``` 或 ```~/.bashrc``` 或 ```~/.profile``` 等 登录时 执行的脚本中 
```shell
#bash-complete-gen-from-help
export PATH=$PATH:/app/bash-simplify/bash-complete-gen-from-help/bin/
source /app/bash-simplify/bash-complete-gen-from-help/script/bash-complte--helpTxt2bashComplete.sh
#以自安装miniconda环境中的python运行 此脚本，不影响系统自带python
alias helpTxt2bashComplete.py='/app/Miniconda3-py310_22.11.1-1/bin/python /app/bash-simplify/bash-complete-gen-from-help/bin/helpTxt2bashComplete.py'

```


之后 打开bash终端, 输入 ```helpT<tab><tab>``` 即可获得补全为 helpTxt2bashComplete.py，  再输入 ```--<tab><tab>``` 再次获得提示

