# 亚马逊搜索爬虫(抓取Currently unavailable.)

## 虚拟环境配置

**创建** 

```bash
python -m venv venv
```

**激活**

```bash
cd venv/scripts
./activate(windows) or source activate(linux or mac)
```


## 环境配置

配置阿里云镜像源

```
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
``` 

或者配置清华源

```
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

## 安装依赖

```
pip install -r requirements.txt
```

## 运行
启动图形界面

```
python gui.py
```

测试

```
python -m unittest tests/index_test.py
```


