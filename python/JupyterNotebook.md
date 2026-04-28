Jupyter Notebook 界面是一个基于 Web 的应用程序，用于创作将实时代码与叙述性文本、公式和可视化相结合的文档。


## 在Conda 中安装Jupyter Notebook

安装Anaconda或Miniconda任选一个
```
#curl -O https://repo.anaconda.com/archive/Anaconda3-2025.12-2-Linux-x86_64.sh
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```


```
#bash ./Anaconda3-2025.12-2-Linux-x86_64.sh
bash ./Miniconda3-latest-Linux-x86_64.sh
```
安装完成后，安装程序显示：“感谢您安装 Miniconda3！”
关闭并重新打开终端窗口以使安装完全生效，或者根据您的 shell 版本，使用以下命令刷新终端：
```
source ~/.bashrc
```

验证是否安装成功
```
conda list
```

创建虚拟环境
```
conda create --name jupyter-env python=3.13
```
激活虚拟环境
```
conda activate jupyter-env
```
安装了Jupyter
```
conda install jupyter
```
启动Jupyter
```
jupyter notebook
```

退出虚拟环境
```
conda deactivate  
```