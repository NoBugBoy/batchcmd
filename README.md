# batchcmd批量操作linux主机

### Github
[batchCmd源码](https://github.com/NoBugBoy/batchcmd)   欢迎star~
### 运行环境
需要python3.0+，如需要二进制运行还需要安装pyinstaller

### 安装
1.  clone到本地，修改根目录.cfg配置文件，运行batchCMD.py
2.  clone到本地，安装pyinstaller，执行 pyinstaller -f batchCMD.py ,会生成二进制文件在同级目录下放入.cfg配置文件即可

### 配置文件
支持口令和秘钥两种方式
1. 密码格式：172.16.3.131 -p 密码
2. 私钥模式：172.16.3.131 -key 私钥绝对路径
3. 默认为root,修改用户名：172.16.3.131 -u tyy -p 密码
4. ssh端口使用为22，暂无配置，需要修改可改源码。

### 启动命令
|命令| 说明 |
|--|--|
| -h | 帮助 |
| -i | 开启持续交互式 |
| -g | 指定配置文件的主机组名称 |
| -c | shell命令（top等持续输出命令请加输出次数否则会不显示 ） |
| -fun | 指定函数，目前支持put和get分别为sftp上传下载 |
| -form | 配合fun的put或get使用，指定原始文件目录 |
| -to | 配合fun的put或get使用，指定目标文件目录  |
| 交互中输入 cc | 等同于【ctrl + c】 |


源码模式: 
```python
python3 bashCMD.py  -g web -i -c 'ls'
python3 bashCMD.py -g web -fun put -form /home/123.txt -to /home/123.txt
python3 bashCMD.py -g web -fun get -form /home/123.txt -to /home/123.txt
```
二进制模式：
```python
./bashCMD -g web -i -c 'ls'
./bashCMD -g web -fun put -form /home/123.txt -to /home/123.txt
./bashCMD -g web -fun get -form /home/123.txt -to /home/123.txt
```
