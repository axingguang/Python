# 堡垒机配置
blj = {
    "blip": "115.182.63.65",
    "bluser": "username",#堡垒机用户名
    "blpasswd": "mima",#堡垒机密码
    "timeout": 10
}
#默认等录服务器用户名
defaultUname="服务器用户名"
#默认登录服务的密码
defaultUpasswd="服务器密码"
#暂未使用
ipList = [
    ('10.154.80.213', "服务器用户名", "服务器密码"),
    ('10.154.81.24', "服务器用户名", "服务器密码"),
    ('10.154.81.2', "服务器用户名", "服务器密码")
]
#日志路径
logpath = "/mine/workspace/log/test1.log"
#默认记录返回信息路径
cmdInfoPath = "/mine/workspace/cmdInfo"
#downPath = "/mine/workspace/down"

operatList = [
    "1:执行命令，返回完整信息，如:ls",
    "2:执行命令，返回实时信息，如：dstat",
    "exit:返回上一层或退出"
]
