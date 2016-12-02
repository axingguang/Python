
from loginLinux import *
import _thread as thread
import time
import sys

inputIpplist = []
inputUsername = ''
inputPassword = ''


def send_cmd(blj_v):
    listChannel={}
    while True:
        cmd = input("请输入命令：")

        for ipInfo in inputIpplist:
            hostname = ipInfo
            user = defaultUname
            password = defaultUpasswd

            if hostname in listChannel:
                channel = listChannel[hostname]
            else:
                channel = blj_v.create_channel(user, hostname, password)
                listChannel[hostname] = channel
            channel.send(cmd + "\n")
            buff = ''
            try:
                while buff.find("# ") == -1 and buff.find("$ ") == -1:
                    resp = str(channel.recv(9999), encoding="utf8")
                    buff += resp
                    print(hostname+":"+resp)
            except Exception as e:
                print(hostname+":error info:" + str(e))
            if cmd == "exit":
                channel.close()
                break

        if cmd == "exit":
            listChannel.clear()
            break


def send_cmd_thread(blj_v,cmd,user, hostname, password):
    channel = blj_v.create_channel(user, hostname, password)
    channel.send(cmd + "\n")
    buff = ''
    try:
        while buff.find("# ") == -1 and buff.find("$ ") == -1:
            resp = str(channel.recv(9999), encoding="utf8")
            buff += resp
            if len(hostname) < 15:
                for i in (len(hostname), 15):
                    hostname += " "
            print(hostname+":"+resp)
    except Exception as e:
        print(hostname+":error info:" + str(e))

    channel.close()


def run_thread(blj_v):
    cmd = input("请输入命令：")
    if cmd == "exit":
        return
    for ipInfo in inputIpplist:
        hostname = ipInfo
        user = defaultUname
        password = defaultUpasswd
        try:
            thread.start_new_thread(send_cmd_thread, (blj_v, cmd, user, hostname, password))
        except:
            print("Error: unable to start thread")


if __name__ == "__main__":

    ipliststr = input("录入ip列表，以‘,’隔开：")
    if ipliststr == '':
        print("ip列表错误，退出")
        sys.exit()
    inputIpplist = ipliststr.split(",")


    blj = LoginBlj()

    while True:
        print("按照以下说明录入对应的编码：")

        for fwList in operatList:
            print(fwList)
        val = input("编码：")
        if val == "1":
            send_cmd(blj)

        if val == "2":
            run_thread(blj)

        if val == "exit":
            break

    blj.close_blj()



