from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import time,  sched
import _thread as thread

from util import *


root = Tk()
root.title("socket")
root.geometry("600x600")
frm=Frame(root)

def connect():
    filepathV = filepathTxt.get()
    filepathV = filepathV.strip()

    if not filepathV:
        outTxt.insert(END, "请录入dubbo服务ip列表文件路径\n")
        return
    outTxt.insert(END, "文件路径：" + filepathV + "\n")
    fo = open(filepathV, 'r')
    line = fo.readline()
    line = line.strip()
    listIP = []
    while line:
        listIP.append(line)
        line = fo.readline()
    selectSv = serviceList.get()
    if "请选择" == selectSv or selectSv == '':
        outTxt.insert(END, "请选择service\n")
        return
    outTxt.insert(END, "服务:" + selectSv + "\n")

    selectMv = methodList.get()
    if "请选择" == selectMv or selectMv == '':
        outTxt.insert(END, "请选择method\n")
        return
    outTxt.insert(END, "接口:" + selectMv + "\n")
    paramV = paramTxt.get()
    outTxt.insert(END, "参数:" + paramV + "\n")
    if paramV == '':
        selectMv = selectMv + "()"
    else:
        selectMv = selectMv + "(" + paramV + ")"
    for host in listIP:
        ip,port = host.split(":")
        thread.start_new_thread(invoke_thread, (ip.strip(), port.strip(), selectSv, selectMv))

def invoke_thread(ip, port, selectSv, selectMv):
    try:
        res = get_method_return(ip, port, selectSv, selectMv)
        res_arr = res.split(",")
        outTxt.insert(END, ip + ":" + str(port) + "=========>" + res_arr[0] + "\n\n")
    except Exception as e:
        outTxt.insert(END, "error:" + str(e) + "\n")

def testconnect():

    selectV = hostList.get()
    if "请选择" == selectV or selectV == '':
        outTxt.insert(END, "请选择IP\n")
        return
    arr = selectV.split(" ")
    ip = arr[0].strip()
    port = arr[1].strip()
    outTxt.insert(END, "ip:" + ip + "\n")
    outTxt.insert(END, "端口:" + port + "\n")

    selectSv = serviceList.get()
    if "请选择" == selectSv or selectSv == '':
        outTxt.insert(END, "请选择service\n")
        return
    outTxt.insert(END, "服务:" + selectSv + "\n")

    selectMv = methodList.get()
    if "请选择" == selectMv or selectMv == '':
        outTxt.insert(END, "请选择method\n")
        return

    outTxt.insert(END, "接口:" + selectMv + "\n")
    paramV = paramTxt.get()
    outTxt.insert(END, "参数:" + paramV + "\n")

    if paramV == '':
        selectMv = selectMv + "()"
    else:
        selectMv = selectMv + "(" + paramV + ")"
    outTxt.insert(END, "连接测试开始===============================\n")
    try:
        res = get_method_return(ip, port, selectSv, selectMv)
    except Exception as e:
        outTxt.insert(END, str(2) + "\n")
    else:
        res_arr = res.split(",")
        outTxt.insert(END, res_arr[0] + "\n")

    outTxt.insert(END, "连接测试结束===============================\n")
    outTxt.insert(END, "---------------------------------------------------------------------------\n")


def selectserver(*args):
    selectV=serverList.get()
    hostListV = servers[selectV]
    hostList.set("请选择")
    hostList["values"] = tuple(hostListV)
    serviceList.set("请选择")
    methodList.set("请选择")

def selectHost(*args):
    selectV=hostList.get()
    arr = selectV.split(" ")
    ip = arr[0]
    port = arr[1]
    try:
        res = get_service(ip.strip(),port.strip())
    except Exception as e:
        outTxt.insert(END, "" + str(e) + "\n")
        return
    res_arry = res.split("\r\n")
    res_arry.pop()
    serviceList.set("请选择")
    serviceList["values"] = tuple(res_arry)
    methodList.set("请选择")

def selectService(*args):
    selectV = hostList.get()
    arr = selectV.split(" ")
    ip = arr[0]
    port = arr[1]
    selectSv=serviceList.get()
    res=get_method(ip.strip(),port.strip(),selectSv)
    res_arry = res.split("\r\n")
    res_arry.pop()
    methodList.set("请选择")
    methodList["values"] = tuple(res_arry)


def loadfile(*args):
    filepathV = filepathTxt.get()
    filepathV = filepathV.strip()

    if not filepathV:
        outTxt.insert(END,"请录入dubbo服务ip列表文件路径\n")
        return
    outTxt.insert(END, "文件路径：" + filepathV + "\n")
    fo = open(filepathV,'r')

    line = fo.readline()
    line = line.strip()
    listIP = []
    while line:
        line = line.replace(":", " ")
        listIP.append(line)
        line = fo.readline()
    hostList.set("请选择")
    hostList["values"] = tuple(listIP)


def selectFile(*args):
    fname = askopenfilename(filetypes=(("Text file", "*.txt"), ("", "")))
    var.set(fname)


schedule = sched.scheduler(time.time, time.sleep)
jobStatus = False

def perform_command( cmd,inc):
    # 安排inc秒后再次运行自己，即周期运行
    if jobStatus:
        schedule.enter(inc, 0, perform_command, (cmd, inc))
        connect()


def timming_exe( cmd, inc):
    # enter用来安排某事件的发生时间，从现在起第n秒开始启动
    schedule.enter(inc, 0, perform_command, (cmd, inc))
    # 持续运行，直到计划时间队列变成空为止
    schedule.run()


def begin_job(*args):
    timeV = timeTxt.get()
    timeV = timeV.strip()
    if not timeV:
        outTxt.insert(END, "请录入执行周期时间（s）\n")
        return
    intTimeV = int(timeV)
    global jobStatus
    jobStatus = True
    thread.start_new_thread(timming_exe, ("aa", intTimeV))


def end_job(*args):
    global jobStatus
    jobStatus = False


frm_top_top=Frame(frm,width=600,height=20)
filepathLab=Label(frm_top_top,text="FILEPATH",width=10,height=2)
filepathLab.pack(side=LEFT)
var = StringVar()
filepathTxt = Entry(frm_top_top, width=39, textvariable=var)

filepathTxt.pack(side=LEFT)

seletFilebuttn = Button(frm_top_top, text="选择文件", command=selectFile)
seletFilebuttn.pack(side=LEFT)
loadbuttn = Button(frm_top_top, text="加载", command=loadfile)
loadbuttn.pack(side=LEFT)



frm_top_top.pack(side=TOP)

frm_top=Frame(frm,width=600,height=20)
hostLab=Label(frm_top,text="IP",width=10,height=2)
hostLab.pack(side=LEFT)

hostList = ttk.Combobox(frm_top,width=50)
# hostList=Listbox(frm_top,width=50)
hostList["state"] = "readonly"
hostList.set("请选择")

hostList.bind("<<ComboboxSelected>>", selectHost)

hostList.pack(side=LEFT)

frm_top.pack(side=TOP)


frm_second=Frame(frm,width=600,height=20)
serviceLab=Label(frm_second,text="SERVICE",width=10,height=2)
serviceLab.pack(side=LEFT)

serviceList = ttk.Combobox(frm_second,width=50)
serviceList["state"] = "readonly"
serviceList.pack(side=LEFT)
serviceList.set("请选择")
serviceList.bind("<<ComboboxSelected>>", selectService)
frm_second.pack(side=TOP)


frm_third=Frame(frm,width=600,height=20)
methodLab=Label(frm_third,text="METHOD",width=10,height=2)
methodLab.pack(side=LEFT)

methodList=ttk.Combobox(frm_third,width=50)
methodList["state"] = "readonly"
methodList.pack(side=LEFT)
methodList.set("请选择")
frm_third.pack(side=TOP)


frm_forth = Frame(frm, width=600, height=20)
paramLab = Label(frm_forth, text="PARAM", width=10, height=2)
paramLab.pack(side=LEFT)

paramTxt = Entry(frm_forth, width=53)
paramTxt.pack(side=LEFT)


frm_forth.pack(side=TOP)


frm_five = Frame(frm, width=600, height=20)
testbuttn = Button(frm_five, text="连接测试", command=testconnect)
testbuttn.pack(side=LEFT)
buttn = Button(frm_five, text="扫描服务", command=connect)
buttn.pack(side=LEFT)
frm_five.pack(side=TOP)

frm_six = Frame(frm, width=600, height=20)
timeLab = Label(frm_six, text="job执行周期（s）", width=14, height=2)
timeLab.pack(side=LEFT)

timeTxt = Entry(frm_six, width=40)
timeTxt.pack(side=LEFT)
startbuttn = Button(frm_six, text="启动job", command=begin_job)
startbuttn.pack(side=LEFT)
stopbuttn = Button(frm_six, text="停止job", command=end_job)
stopbuttn.pack(side=LEFT)
frm_six.pack(side=TOP)

frm_bottom = Frame(frm)
outTxt = Text(frm_bottom,width=200,height=200)


scrl = Scrollbar(frm_bottom)

scrl.pack(side=RIGHT, fill=Y)
outTxt.configure(yscrollcommand = scrl.set)
# lb.pack(side=LEFT, fill=BOTH)

outTxt.pack()
scrl['command'] = outTxt.yview

frm_bottom.pack(side=BOTTOM)
frm.pack()

root.mainloop()


