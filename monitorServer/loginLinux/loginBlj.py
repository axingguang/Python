#!/usr/bin/env python
import paramiko
import os,sys,time
from .conf import *


class LoginBlj():
    def __init__(self):
        self.blip = blj['blip']
        self.bluser = blj['bluser']
        self.blpasswd = blj['blpasswd']
        self.port = 22
        self.logPath = logpath
        self.passinfo = "'s password: "
        self.timeout = blj['timeout']
        paramiko.util.log_to_file(self.logPath)

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.blip, username=self.bluser, password=self.blpasswd)

    def create_channel(self, user, hostname, password):
        channel = self.ssh.invoke_shell()
        channel.settimeout(self.timeout)

        buff = ""
        resp = ""
        channel.send("ssh " + user + "@" + hostname + "\n")

        while not buff.endswith(self.passinfo):
            try:
                resp = str(channel.recv(9999), encoding="utf8")
            except Exception as e:
                print('Error info:%s connection time.' % (str(e)))
                channel.close()
            buff += resp
            if not buff.find("yes/no") == -1:
                channel.send("yes\n")
                buff = ''
        channel.send(password + "\n")

        buff = ''

        while not buff.endswith("# ") and not buff.endswith("$ "):
            resp = str(channel.recv(9999), encoding="utf8")

            if not resp.find(self.passinfo) == -1:
                print('Error info:Authentication failed.')
                channel.close()
            buff += resp
        print(hostname+"：连接已建立")
        return channel

    def close_blj(self):
        self.ssh.close()
