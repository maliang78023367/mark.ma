import _thread
import time
import sys,os

#fpath="c:\\Python36\\test\\print_time_file.txt"
fpath="c:\\python36\\test\\mike.log"
mike_log="C:\\Users\\FVT2\\Desktop\\Mike_Log\\Mike_HibernationResume_auto_20181012-2133.log"
g_fileinfo=0.0
g_times=0
g_Ping_Times=3




####################################################
def api_writefile(ss=''):

    # log file path
    g_CurrentPath = os.getcwd()
    path = g_CurrentPath+"\\log.txt"
    
    with open(path,'a') as log_file:
        log_file.write(ss+'\n')
        print(ss)

####################################################
def check_device(out=""):
    g_CurrentPath = os.getcwd()
    #============================
    # check HWID
    #print( os.popen("cd Python36\test") )
    #p=os.popen("cd \\ &&cd python36\\restart && check_hwid.bat")
    cmd = "cd \\ &&cd " +g_CurrentPath+ " && check_hwid.bat"
    p=os.popen(cmd)
    time.sleep(5)#wait 2s
    path = g_CurrentPath + "\\check_hwid.log"
    with open(path,'r') as check_hwid:
        str_check_hwid=check_hwid.read()
    
        if str_check_hwid.find("PCIe-OK")!=-1:
            api_writefile("====== " +out+ " PCIe SUCCESS ======\n")
        else:
            api_writefile("====== " +out+ " PCIe FAIL ======\n")

    
        if str_check_hwid.find("ModemCtl-OK")!=-1:
            api_writefile("====== " +out+ " ModemCtl SUCCESS ======\n")
        else:	
            api_writefile("====== " +out+ " ModemCtl FAIL ======\n")

            
        if str_check_hwid.find("MBIM-OK")!=-1:
            api_writefile("====== " +out+ " MBIM SUCCESS ======\n")
        else:
            api_writefile("====== " +out+ " MBIM FAIL ======\n")

                    
                    
        cmd = "devcon.exe  hwids * > devcon.log"
        admin_cmd="admin_checkDev.bat"
        p=os.popen(admin_cmd)
        time.sleep(5)#wait 2s
        devcon_log = g_CurrentPath + "\\devcon.log"
        with open(devcon_log,'r') as devcon:
            devcon_str=devcon.read()
            #print(devcon_str)
            if devcon_str.find("FWUpdateDriver Device")!=-1:
                api_writefile("====== " +out+ " FWUpdateDriver SUCCESS ======\n")
            else:
                api_writefile("====== " +out+ " FWUpdateDriver FAIL ======\n")
                

    os.popen("del "+ path)
    path = g_CurrentPath + "\\devcon.log"
    os.popen("del "+ path)

####################################################
def check_ping(times=g_Ping_Times, out=""):
    g_CurrentPath = os.getcwd()
    cmd_Ping="@ping -n 10 www.baidu.com"
    cmd_DeviceInfo="netsh mbn show interfaces"
    cnt=0
    
    os.popen("netsh wlan disconnect")
    for i in range(0,times):
        time.sleep(15)
        
        #====================================
        # show cellular infop
        p=os.popen(cmd_DeviceInfo)
        str_return=p.read()
        api_writefile(str_return)
        
        #====================================
        # Ping		
        p=os.popen(cmd_Ping)
        str_return=p.read()
        api_writefile( str_return )
        if (str_return.find("(100% loss)"))==-1 and (str_return.find("could not find"))==-1:
            api_writefile("====== " +out+ " PING SUCCESS ======\n")
            break;
        else:
            cnt = cnt + 1
            
    if cnt>=times:
        api_writefile("====== " +out+ " PING Fail ======\n")


####################################################
# 为线程定义一个函数
def print_time( threadName, delay):
    g_fileinfo=0.0
    fileinfo = 0.0
    count = 0
    mikelog_start=0
    g_times=0
    fpath="c:\\python36\\test\\mike.log"
    
    mikelog_path = os.listdir("C:\\Users\\FVT2\\Desktop\\Mike_Log")
    print(mikelog_path)
    mikelog_path2 = "C:\\Users\\FVT2\\Desktop\\Mike_Log\\" + str(mikelog_path)[2:-2]
    
    while 1:
        time.sleep(delay)
        count += 1
        #print("%s: %s" % ( threadName, time.ctime(time.time()) ))
        #print(fpath)
        #print( os.path.getmtime(fpath) )
        p=os.popen("copy " +mikelog_path2+ " c:\\python36\\test\\mike.log")
        #print("copy " +mikelog_path2+ " c:\\python36\\test\\mike.log")
        fpath="c:\\python36\\test\\mike.log"
        print(".", end=' ')
    
    
        fileinfo=os.path.getmtime(fpath)
        if fileinfo > g_fileinfo:
            try:
                with open("c:\\Python36\\test\\mike.log",'r') as mike_file:
                    mike_log = mike_file.read()
                    start =  mike_log.find("Resume counter = ",mikelog_start)
                    if start==-1:
                        continue
                    mikelog_start = start+1
                    end = mike_log.find("\n",start)
                    if end==-1:
                        continue
                    
                    
                    times=int( mike_log[start+len("Resume counter = "):end] )
                    print( times )
                    api_writefile("Resume counter = "+str(times))
                    
                    if g_times!=times:
                        g_fileinfo = fileinfo
                        g_times = times
                        do_something()
            except:
                pass
        
        
####################################################
def do_something():	
    api_writefile("\n\n\n==========================="):
    api_writefile("============ START ==============="):
    api_writefile("==========================="):
    check_device(out="S4")
    check_ping(3, out="S4")
    api_writefile("==========================="):
    api_writefile("=========== END ================"):
    api_writefile("==========================="):

if __name__ == "__main__":
    _thread.start_new_thread( print_time, ("Thread-1", 3, ) )
    #do_something()
    while 1:
        pass
        
        

import _thread
import time
import sys,os

#fpath="c:\\Python36\\test\\print_time_file.txt"
fpath="c:\\python36\\test\\mike.log"
mike_log="C:\\Users\\FVT2\\Desktop\\Mike_Log\\Mike_HibernationResume_auto_20181012-2133.log"
g_fileinfo=0.0
g_times=0
g_Ping_Times=3




####################################################
def api_writefile(ss=''):

    # log file path
    g_CurrentPath = os.getcwd()
    path = g_CurrentPath+"\\log.txt"
    
    with open(path,'a') as log_file:
        log_file.write(ss+'\n')
        print(ss)

####################################################
def check_device(out=""):
    g_CurrentPath = os.getcwd()
    #============================
    # check HWID
    #print( os.popen("cd Python36\test") )
    #p=os.popen("cd \\ &&cd python36\\restart && check_hwid.bat")
    cmd = "cd \\ &&cd " +g_CurrentPath+ " && check_hwid.bat"
    p=os.popen(cmd)
    time.sleep(5)#wait 2s
    path = g_CurrentPath + "\\check_hwid.log"
    with open(path,'r') as check_hwid:
        str_check_hwid=check_hwid.read()
    
        if str_check_hwid.find("PCIe-OK")!=-1:
            api_writefile("====== " +out+ " PCIe SUCCESS ======\n")
        else:
            api_writefile("====== " +out+ " PCIe FAIL ======\n")

    
        if str_check_hwid.find("ModemCtl-OK")!=-1:
            api_writefile("====== " +out+ " ModemCtl SUCCESS ======\n")
        else:	
            api_writefile("====== " +out+ " ModemCtl FAIL ======\n")

            
        if str_check_hwid.find("MBIM-OK")!=-1:
            api_writefile("====== " +out+ " MBIM SUCCESS ======\n")
        else:
            api_writefile("====== " +out+ " MBIM FAIL ======\n")

                    
                    
        cmd = "devcon.exe  hwids * > devcon.log"
        p=os.popen(cmd)
        time.sleep(5)#wait 2s
        devcon_log = g_CurrentPath + "\\devcon.log"
        with open(devcon_log,'r') as devcon:
            devcon_str=devcon.read()
            #print(devcon_str)
            if devcon_str.find("FWUpdateDriver Device")!=-1:
                api_writefile("====== " +out+ " FWUpdateDriver SUCCESS ======\n")
            else:
                api_writefile("====== " +out+ " FWUpdateDriver FAIL ======\n")
                

                        
    os.popen("del "+ path)
    os.popen("del "+ devcon_log)

####################################################
def check_ping(times=g_Ping_Times, out=""):
    g_CurrentPath = os.getcwd()
    cmd_Ping="@ping -n 10 www.baidu.com"
    cmd_DeviceInfo="netsh mbn show interfaces"
    cnt=0
    
    os.popen("netsh wlan disconnect")
    for i in range(0,times):
        time.sleep(15)
        
        #====================================
        # show cellular infop
        p=os.popen(cmd_DeviceInfo)
        str_return=p.read()
        api_writefile(str_return)
        
        #====================================
        # Ping		
        p=os.popen(cmd_Ping)
        str_return=p.read()
        api_writefile( str_return )
        if (str_return.find("(100% loss)"))==-1 and (str_return.find("could not find"))==-1:
            api_writefile("====== " +out+ " PING SUCCESS ======\n")
            break;
        else:
            cnt = cnt + 1
            
    if cnt>=times:
        api_writefile("====== " +out+ " PING Fail ======\n")


####################################################
# 为线程定义一个函数
def print_time( threadName, delay):
    g_fileinfo=0.0
    fileinfo = 0.0
    count = 0
    mikelog_start=0
    g_times=0
    fpath="c:\\python36\\test\\mike.log"
    
    mikelog_path = os.listdir("C:\\Users\\FVT2\\Desktop\\Mike_Log")
    print(mikelog_path)
    mikelog_path2 = "C:\\Users\\FVT2\\Desktop\\Mike_Log\\" + str(mikelog_path)[2:-2]
    
    while 1:
        time.sleep(delay)
        count += 1
        #print("%s: %s" % ( threadName, time.ctime(time.time()) ))
        #print(fpath)
        #print( os.path.getmtime(fpath) )
        p=os.popen("copy " +mikelog_path2+ " c:\\python36\\test\\mike.log")
        #print("copy " +mikelog_path2+ " c:\\python36\\test\\mike.log")
        fpath="c:\\python36\\test\\mike.log"
        print(".", end=' ')
    
    
        fileinfo=os.path.getmtime(fpath)
        if fileinfo > g_fileinfo:
            try:
                with open("c:\\Python36\\test\\mike.log",'r') as mike_file:
                    mike_log = mike_file.read()
                    start =  mike_log.find("Resume counter = ",mikelog_start)
                    if start==-1:
                        continue
                    mikelog_start = start+1
                    end = mike_log.find("\n",start)
                    if end==-1:
                        continue
                    
                    
                    times=int( mike_log[start+len("Resume counter = "):end] )
                    print( times )
                    api_writefile("Resume counter = "+str(times))
                    
                    if g_times!=times:
                        g_fileinfo = fileinfo
                        g_times = times
                        do_something()
            except:
                pass
        
        
####################################################
def do_something():	
    api_writefile("\n\n\n==========================="):
    api_writefile("============ START ==============="):
    api_writefile("==========================="):
    check_device(out="S3")
    check_ping(3, out="S3")
    api_writefile("==========================="):
    api_writefile("=========== END ================"):
    api_writefile("==========================="):

if __name__ == "__main__":
    _thread.start_new_thread( print_time, ("Thread-1", 3, ) )
    #do_something()
    while 1:
        pass
        
        

