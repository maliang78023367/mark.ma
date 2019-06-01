import _thread
import time
import sys,os

#fpath="c:\\Python36\\test\\print_time_file.txt"
fpath="c:\\python36\\test\\mike.log"
mike_log="C:\\Users\\FVT2\\Desktop\\Mike_Log\\Mike_HibernationResume_auto_20181012-2133.log"
g_fileinfo=0.0
g_times=0
g_Flag_Suspend=0
g_Ping_Times=3
g_interfaces_name=''


####################################################
def check_restart():
    api_writefile( "\n\n\n==============================================" )
    api_writefile( "==============================================" )
    api_writefile( "================= START ======================" )
    api_writefile(str( time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) )+"\n\n")
    
    
####################################################
def check_end():
    api_writefile("\n\n"+str( time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) ))
    api_writefile( "=================== END ======================" )
    api_writefile( "==============================================" )
    api_writefile( "==============================================\n\n\n" )


####################################################
def api_writefile(ss=''):

    # log file path
    path = g_CurrentPath+"\\log.txt"
    
    with open(path,'a') as log_file:
        log_file.write(ss+'\n')
        print(ss)


####################################################
def check_device(out=""):
    
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
            # g_Err_cnt=g_Err_cnt+1
            if g_Flag_Suspend==1:
                os.popen("del "+ path)
                while(1):
                    pass
    
        if str_check_hwid.find("ModemCtl-OK")!=-1:
            api_writefile("====== " +out+ " ModemCtl SUCCESS ======\n")
        else:	
            api_writefile("====== " +out+ " ModemCtl FAIL ======\n")
            # g_Err_cnt=g_Err_cnt+1
            if g_Flag_Suspend==1:
                os.popen("del "+ path)
                while(1):
                    pass
            
        if str_check_hwid.find("MBIM-OK")!=-1:
            api_writefile("====== " +out+ " MBIM SUCCESS ======\n")
        else:
            api_writefile("====== " +out+ " MBIM FAIL ======\n")
            # g_Err_cnt=g_Err_cnt+1
            if g_Flag_Suspend==1:
                os.popen("del "+ path)
                while(1):
                    pass
                    
    os.popen("del "+ path)


####################################################
def check_ping(times=g_Ping_Times, out=""):

    cmd_Ping="@ping -n 10 www.baidu.com"
    cmd_DeviceInfo="netsh mbn show interfaces"
    cnt=0
    
    popen("netsh wlan disconnect")
    for i in range(0,times):
        time.sleep(6)
        
        #====================================
        # show cellular infop
        p=os.popen(cmd_DeviceInfo)
        str_return=p.read()
        api_writefile(str_return)
        
        start = str_return.find( "Name                   : " )
        end = str_return.find( "\n",start )
        s=str_return[ start+len("Name                   : "):end ]
        print(g_interfaces_name)
        
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
        # g_Err_cnt=g_Err_cnt+1
        if g_Flag_Suspend==1:
            while(1):
                pass
    

# 为线程定义一个函数
def print_time( threadName, delay ):
    g_fileinfo=0.0
    fileinfo = 0.0
    count = 0
    mikelog_start=0
    g_times=0
    
    
    fpath=g_CurrentPath + "\\mike.log"
    
    
    mikelog_path = os.listdir("C:\\Users\\FVT2\\Desktop\\Mike_Log")
    print(mikelog_path)
    mikelog_path2 = "C:\\Users\\FVT2\\Desktop\\Mike_Log\\" + str(mikelog_path)[2:-2]
    
    while 1:
        time.sleep(delay)
        count += 1
        #p=os.popen("copy " +mikelog_path2+ " c:\\python36\\test\\mike.log")
        p=os.popen("copy " +mikelog_path2+ " "+ g_CurrentPath +"\\mike.log")
        
        #print("====")
        #print("copy " +mikelog_path2+ " "+ g_CurrentPath +"\\mike.log")
        #print(fpath)
        #print("====")

        print(".", end=' ')
    
        time.sleep(2)
        fileinfo=os.path.getmtime(fpath)
        if fileinfo > g_fileinfo:
            with open(fpath,'r') as mike_file:
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
                
                if g_times!=times:
                    g_fileinfo = fileinfo
                    g_times = times
                    api_writefile( "Resume counter = "+str(g_times) )
                    do_something()

                    
                    
def do_something():
    check_restart()
    #time.sleep(20)#wait 2s
    #check_device(out="S4")
    #check_ping(out="S4")
    check_end()

    
    
if __name__ == "__main__":
    g_CurrentPath = os.getcwd()
    g_Flag_Suspend=0
    g_Ping_Times=3
    g_interfaces_name=''

    
    
    cmd_DeviceInfo="netsh mbn show interfaces"
    hibernate = g_CurrentPath + "\\Tool\\pwrtest.exe /sleep /c:1 /s:4 /d:30 /p:20"
    p=os.popen(hibernate)
    print(g_interfaces_name)
    

    p=os.popen(cmd_DeviceInfo)
    str_return=p.read()
    start = str_return.find( "Name                   : " )
    end = str_return.find( "\n",start )
    g_interfaces_name=str_return[ start+len("Name                   : "):end ]
    print(g_interfaces_name)
    
    
    #do_something()
    #print_time('loop', 2)
    #_thread.start_new_thread( print_time, ("Thread-1", 2, ) )
    #_thread.start_new_thread( print_time_file, ("Thread-2", 4, ) )
    #_thread.start_new_thread( show_progress, ("Thread-3", 1, ) )


