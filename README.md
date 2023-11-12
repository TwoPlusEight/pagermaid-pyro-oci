## 甲骨文云流量信息查看

---
### 作用
配合Pagermaid人形, 便捷查看甲骨文云实例对应的网卡出站流量, 或向大🔥展示你的成绩(

### 查看范围
当前租户下的当前区域的实例对应的网卡与存储桶出站流量月度统计  
*(没有全区号或升级号不清楚是否能够统计到其他区域的实例流量)*

### 食用方法
默认情况下在聊天内发送`,obdt`即可查看本月出站流量  
命令列表:  
`,obdt last/l/previous/p` 获取上月出站流量  
`,obdt this/current/t/c` 获取本月月出站流量

### 限制  

需要配合Pagermaid-pyro食用  
每月初会出现单个网卡两个数据的问题

---
### 安装
#### 1. 安装Pagermaid-pyro
**如您从未安装过使用过且注册时间在2022年之后, 登录Pagermaid-pyro将可能被立即封号**  
安装步骤可以参考[PGM-Pyro官方](https://xtaolabs.com/#/?id=%e7%ae%80%e4%bb%8b)的文档进行安装, 此处不再追述  
>**安装后请同时安装python-oci**,安装命令: `pip install oci`

#### 2. 获取甲骨文API
登录甲骨文云, 右上角上半身头像点击*我的概要信息*  
![My_profile](https://img10.360buyimg.com/babel/jfs/t20251111/228040/12/2983/9491/654fb13cFcefe9f98/85141eb6c2f134c3.jpg)  

找到*API密钥*并添加API密钥  
![API_key](https://img10.360buyimg.com/babel/jfs/t20251111/128518/36/36398/33242/654fb13cF8d1664ff/59ea0c4fc9a8986a.jpg)  
下载私钥, 添加  
![add_API_key](https://img10.360buyimg.com/babel/jfs/t20251111/191320/33/42588/57089/654fb13eFd589131f/c715f67b0d58c7d1.jpg)  

复制显示的配置文件预览  
![copy_config](https://img10.360buyimg.com/babel/jfs/t20251111/237348/15/2738/61363/654fb13cF2373cd2e/f66b02b447b8a5c0.jpg)  

新建文件粘贴配置文件预览的内容  
编辑`key_file`, 添加将要存放在pgm服务器的私钥路径(建议使用绝对路径, 即`/root/xxx/xxx`)  
![save_config](https://img10.360buyimg.com/babel/jfs/t20251111/236383/14/2675/17138/654fb13eFdd2d1cc2/9452dca201656322.jpg)  

将私钥配置文件上传服务器

#### 3. 向PGM添加本功能
下载本项目的`oracle_obdt.py`文件, 下载后右键使用文本文档(你有更好的文本编辑文件就用你自己的)编辑本项目的文件  
将以下内容更改为自己配置文件的路径, 配置文件的名称, 查询时激活本项目文件的命令  
![edit_file](https://img10.360buyimg.com/babel/jfs/t20251111/192515/32/40567/23677/654fb13eF110c30cc/7ba28deadffeb817.jpg)

修改完成后将文件上传至第一步存放pagermaid文件夹内的plugins文件夹  
即`你安装pagermaid的文件夹/plugins/`

#### 4. 重载pagermaid
在聊天内输入`,reload`即可刷新模块, 输入`,help`即可找到默认的命令或你修改后的命令名称

### 不足
原为自用的功能, 应群友疑问特此公开  
代码较为粗糙, 仅达到可用的状态, 敬请谅解  
另付自用的功能, 由于过于粗糙并不开放使用, 仅供参考  
![another_function](https://img10.360buyimg.com/babel/jfs/t20251111/195006/36/41322/62535/654fb40bFb80d0d02/1376f9b58ee94bcb.jpg)  
![another_function_limit](https://img10.360buyimg.com/babel/jfs/t20251111/184718/24/42123/24777/654fb46cF97dade93/d4f8563d58b50953.jpg)
