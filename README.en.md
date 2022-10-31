# Ramox

([简体中文](README.md) | English)

### Description

This program is a WeChat bot built based on Flask. This program utilizes [DaenWxHook.dll](DaenWxHook/DaenWxHook.dll), which is developed by Daen, in order to read WeChat activities and send them to localhost. For detailed information, please see its [API document](https://www.apifox.cn/apidoc/project-1222856/). This program only provides an automatic replying framework, and please implement the function that generates replied contents and the message processing algorithms yourself.

### Installation
1. Clone or download this repository.
2. Install Python. Please make sure that you have added Python to PATH.
3. Install Flask with the following command:
```shell
python -m pip install flask -U
```

### Run
1. Install [WeChat 3.6.0.18](WeChatSetup3.6.0.18.exe). This is the only WeChat version that is supported by this program.
2. Implement the "respond" function in [ramox.py](ramox.py). The information of arguments is given in the comments.
3. Run [server.py](server.py).
4. Run [Daen注入器](DaenWxHook/Daen%E6%B3%A8%E5%85%A5%E5%99%A8.exe). This program will activate WeChat and inject [DaenWxHook.dll](DaenWxHook/DaenWxHook.dll) into its process. Please enter the path of the folder that WeChat is in in "文件目录", the path of [DaenWxHook.dll](DaenWxHook/DaenWxHook.dll) in "DLL路径", and callBackUrl=http://localhost:8089/wechat&port=8055&decryptImg=1 in "进程参数".

You can also modify [server.py](server.py) or [ramox.py](ramox.py) to implement more functionalities.
Please notice that the usage of this program might lead to violation of [Agreement on Software License and Service of Tencent Weixin](https://weixin.qq.com/agreement). Please only use this program according to the agreement. We will not be responsible of any legal consequences brought by violation of [Agreement on Software License and Service of Tencent Weixin](https://weixin.qq.com/agreement).

### References
Daen. (2022). _WeChat HOOK HTTP_. https://www.apifox.cn/apidoc/project-1222856