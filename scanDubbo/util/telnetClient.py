import json
import telnetlib


def do_telnet(Host, port, command):
    # try:
    finish = 'dubbo>'
    tn = telnetlib.Telnet(Host, port, timeout=10)
    tn.write(bytes(command+"\n", encoding="utf8"))
    rs = tn.read_until(bytes(finish, encoding="utf8"))
    rs_filter = rs.split(b'elapsed')
    rs_valid = rs_filter[0].strip()
    # re_arr=rs_valid.split(b"\r\n")
    rs_gbk = rs_valid.decode('gbk')
    return rs_gbk
    # except Exception:
    #     print("error")

def get_service(Host, port):
    command = "ls"
    return do_telnet(Host,port, command)

def get_method(Host, port,service):
    command = "ls " +service
    return do_telnet(Host, port, command)

def get_method_return(Host, port,service,method):
    command = "invoke "+service+"."+method
    return do_telnet(Host, port, command)
