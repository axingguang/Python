
from loginLinux import *
import _thread as thread
import threading
import time
import sys
import os

inputIplist = []
inputUsername = ''
inputPassword = ''
listChannel = {}




def send_cmd(blj_v):
    listChannel={}
    while True:
        cmd = input("请输入命令：")
        filename = ''
        recordCmdInfo = False
        if cmd.find(">>") != -1:
            cmd,filename = cmd.split(">>")
            recordCmdInfo = True
            dir = cmdInfoPath+"/"+filename
            of = open(dir,"a")
        else:
            recordCmdInfo = False

        for ipInfo in inputIplist:
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
                print("--------------------------------------"+hostname+"--------------------------------------------")
                if recordCmdInfo:
                    of.write("\n--------------------------------------" + hostname + "--------------------------------------------\n")
                while buff.find("# ") == -1 and buff.find("$ ") == -1:
                    resp = str(channel.recv(9999), encoding="utf8")
                    buff += resp
                    if recordCmdInfo:
                        of.write(resp)
                    print(resp)
                print("\n")
            except Exception as e:
                if recordCmdInfo:
                    of.write(hostname+":error info:" + str(e)+"\n")
                print(hostname+":error info:" + str(e)+"\n")
            if cmd == "exit":
                channel.close()
                break
        if recordCmdInfo:
            of.close()
            recordCmdInfo = False

        if cmd == "exit":
            listChannel.clear()
            break

def send_cmd_thread(blj_v,cmd,user, hostname, password):

    global listChannel
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
            if len(hostname) < 15:
                for i in (len(hostname), 15):
                    hostname += " "

            print(hostname+":"+resp + "\n")

    except Exception as e:
        print(hostname+":error info:" + str(e) + "\n")
    if cmd == "exit":
        channel.close()
    if cmd == "exit":
        listChannel.clear()


def run_thread(blj_v):
    while True:
        cmd = input("请输入命令：")
        for ipInfo in inputIplist:
            hostname = ipInfo
            user = defaultUname
            password = defaultUpasswd
            try:
                thread.start_new_thread(send_cmd_thread, (blj_v, cmd, user, hostname, password))
            except:
                print("Error: unable to start thread")
        if cmd == 'exit':
            break

if __name__ == "__main__":

    ipliststr = input("请输入ip列表，以‘,’隔开：")
    if ipliststr == '':
        print("ip列表错误，退出")
        sys.exit()
    inputIplist = ipliststr.split(",")

    blj = LoginBlj()

    while True:
        print("请选择进程执行模式：")
        print("1:单线程运行")
        print("2:多线程运行")
        print("退出，请录入‘exit’")
        inputStr = input("请输入编号：")
        if inputStr == 'exit':
            break
        if inputStr == "1":
            send_cmd(blj)
        if inputStr == "2":
            run_thread(blj)

    blj.close_blj()



