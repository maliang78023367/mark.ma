﻿import _thread
import sys,os,re,time
import ctypes
import subprocess as sp
import threading



#fpath="c:\\Python36\\test\\Thread_CheckLog_file.txt"
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
    global g_DeviceCheck_while
    player = ctypes.windll.kernel32
    
    #============================
    # check HWID
    #print( os.popen("cd Python36\test") )
    #p=os.popen("cd \\ &&cd python36\\restart && check_hwid.bat")
    cmd = "cd \\ &&cd " +g_CurrentPath+ " && check_hwid.bat"
    p=os.popen(cmd)
    time.sleep(5)#wait 2s
    path = g_CurrentPath + "\\check_hwid.log"
    err_cnt=0
    with open(path,'r') as check_hwid:
        str_check_hwid=check_hwid.read()
    
        if str_check_hwid.find("PCIe-OK")!=-1:
            api_writefile("====== " +out+ " PCIe SUCCESS ======\n")
        else:
            api_writefile("====== " +out+ " PCIe FAIL ======\n")
            err_cnt = err_cnt + 1

    
        if str_check_hwid.find("ModemCtl-OK")!=-1:
            api_writefile("====== " +out+ " ModemCtl SUCCESS ======\n")
        else:	
            api_writefile("====== " +out+ " ModemCtl FAIL ======\n")
            err_cnt = err_cnt + 1

            
        if str_check_hwid.find("MBIM-OK")!=-1:
            api_writefile("====== " +out+ " MBIM SUCCESS ======\n")
        else:
            api_writefile("====== " +out+ " MBIM FAIL ======\n")
            err_cnt = err_cnt + 1
#===========================================
        if g_DeviceCheck_while == 1 :
            if err_cnt != 0:
                Timer_Stop()
                while(1):
                    time.sleep(1)
                    player.Beep(1000,300)
#===========================================
                    
        #p=os.popen("cd \\ &&cd python36\\restart && check_hwid.bat")
        cmd = "devcon.exe  hwids * > devcon.log"
        admin_cmd="admin_checkDev.bat"
        p=os.popen(admin_cmd)
        time.sleep(5)#wait 2s
        devcon_log = g_CurrentPath + "\\devcon.log"
        try:
            with open(devcon_log,'r') as devcon:
                devcon_str=devcon.read()
                #print(devcon_str)
                if devcon_str.find("FWUpdateDriver Device")!=-1:
                    api_writefile("====== " +out+ " FWUpdateDriver SUCCESS ======\n")
                else:
                    api_writefile("====== " +out+ " FWUpdateDriver FAIL ======\n")
        except:
            api_writefile("====== " +out+ " FWUpdateDriver FAIL ======\n")
            pass
                

    os.popen("del "+ path)
    path = g_CurrentPath + "\\devcon.log"
    os.popen("del "+ path)

####################################################
def check_ping(times=6, out=""):
    global g_Ping_while
    global g_Ping_times
    
    
    times=g_Ping_times
    
    player = ctypes.windll.kernel32
    g_CurrentPath = os.getcwd()
    cmd_Ping="@ping -n 10 www.baidu.com"
    cmd_DeviceInfo="netsh mbn show interfaces"
    cnt=0
    
    os.popen("netsh wlan disconnect")
    for i in range(0,times):
        time.sleep(15)
        api_writefile(str( time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) )+"\n\n")
        
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
#===========================================
        if g_Ping_while == 1 :
            Timer_Stop()
            while(1):
                time.sleep(1)
                player.Beep(1000,300)
#===========================================


####################################################		
def call_S3(           Total                = 2000, # resume  times
                       w_time_after_resume  = 30,
                       Ping_Check           = 30,
                       BreakAftError        = 1,
                       SleepTime            = 60
                       ):
        api_writefile("\n\n" + "*"*50)
        api_writefile(str( time.ctime(time.time()) ))
        api_writefile("\nCall S3: S3 cycles  = " + str(Total))
        api_writefile("\nw_time_after_resume = " + str(w_time_after_resume))
        api_writefile("\nPing_Check          = " + str(Ping_Check))
        api_writefile("\nBreakafterror       = " + str(BreakAftError))
        api_writefile("\n" + "-"*50)

        #***check the status of module before testing S4***#
        #api_assert(api1_init_mbn_if_info()==0,BreakAftError)
        #api_assert(api1_check_port()==0,BreakAftError)
        #api_assert(api1_ping_test("www.baidu.com",Ping_Check)>0, BreakAftError)                

		#=======================
		# check os type then get this file path
        if getattr(sys, 'frozen', False):
            path = os.path.dirname(sys.executable)
        elif __file__:
            path = os.path.dirname(__file__)

        path = g_CurrentPath
        hibernate = path + "\\Tool\\pwrtest.exe /sleep /c:1 /s:3 /d:30 /p:%s" % str(SleepTime)
        hibernate = path + "\\Tool\\admin_S3.bat"
        for i in range (0,Total):
            cycle_number = str(i+1) + str('/') + str(Total)
            api_writefile("\n"+"-"*50)
            api_writefile("Entering into S3 cycle: " + cycle_number)
            
            time.sleep(3) #Wait 3 seconds to see the printing log
            
            start = time.clock()
            process = sp.Popen(hibernate, shell = True, stdout = sp.PIPE, stderr = sp.PIPE)
            (output, err) = process.communicate()
            
            elasped = (time.clock()-start)
            api_writefile(str("Exited the S3 cycle: ") + str(i+1))
            api_writefile(str("Approx time into S3 state: ") + str(elasped))
            fail_count=i+1                

            time.sleep(w_time_after_resume) #adding the wait time for the system to resume from the sleep state.
            
            
            #win32api.keybd_event(37,0,0,0)
            #win32api.keybd_event(37,0,win32con.KEYEVENTF_KEYUP,0)

            #here check the MBIM Status
            if g_DeviceCheck_flag==1:
                check_device(out="S3")
            if g_Ping_flag==1:
                check_ping(out="S3")
            
            if i == Total:
                api_writefile("\n[Success]:\nThe S3 test has completed sucessfully")
                return 1

                
####################################################
# 为线程定义一个函数
def Thread_CheckLog( threadName, delay):
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
    api_writefile("\n\n\n===========================")
    api_writefile("============ START ===============")
    api_writefile("===========================")
    check_device(out="S3")
    check_ping(3, out="S3")
    api_writefile("===========================")
    api_writefile("=========== END ================")
    api_writefile("===========================")




g_ude_mdmctl_ril_del_index=1
g_ihvril_del_index=1
g_UsbTrace_del_index=1
def delete_log_resume():
    global g_TelephonyTool_Path
    path_TelephonyTool=g_TelephonyTool_Path
    global g_ude_mdmctl_ril_del_index
    global g_ihvril_del_index
    global g_UsbTrace_del_index

    print( "path_TelephonyTool = ",path_TelephonyTool )
    log_file = os.listdir(path_TelephonyTool)
    log_files = os.listdir(path_TelephonyTool+log_file[-1])
   
    '''
    print("=============================")
    print("=============================")
    print("=============================")
    print(log_file)
    
    # do not delete log if capture coredump file.
    log_files = os.listdir(path_TelephonyTool+log_file[-1])
    print("=============================")
    print("=============================")
    print("=============================")
    print( log_files )

    print("=============================")
    print("=============================")
    print("=============================")
    '''
    
    

    #delete UDE log
    ude_mdmctl_ril_cnt=0
    ihvril_cnt=0
    UsbTrace_cnt=0
    ModemTrace_cnt=0
    for item in log_files:
        if item.find("ude_mdmctl_ril_")!=-1:
            ude_mdmctl_ril_cnt = ude_mdmctl_ril_cnt + 1
        elif item.find("ihvril_")!=-1:
            ihvril_cnt = ihvril_cnt + 1
        elif item.find("UsbTrace_")!=-1:
            UsbTrace_cnt = UsbTrace_cnt + 1
        elif item.find("ModemTrace_")!=-1:
            ModemTrace_cnt = ModemTrace_cnt + 1
            
    print("=============================")
    print("Start delete UDE log")
    #ude_mdmctl_ril_cnt = log_files.count("ude_mdmctl_ril_1")      
    print("ude_mdmctl_ril_cnt = ", ude_mdmctl_ril_cnt)
    if ude_mdmctl_ril_cnt > 10:
        ude_mdmctl_ril_delete_name = "ude_mdmctl_ril_" + str(g_ude_mdmctl_ril_del_index)
        print( "ude_mdmctl_ril_delete_name = ",path_TelephonyTool+log_file[-1]+"\\"+ude_mdmctl_ril_delete_name+".etl" )
        api_writefile( "ude_mdmctl_ril_delete_name = "+path_TelephonyTool+log_file[-1]+"\\"+ude_mdmctl_ril_delete_name+".etl" )
        os.popen( "del /S /Q "+path_TelephonyTool+log_file[-1]+"\\"+ude_mdmctl_ril_delete_name+".etl"  )
        g_ude_mdmctl_ril_del_index = g_ude_mdmctl_ril_del_index + 1


    print("=============================")
    print("Start delete RIL log")
    #delete UDE log
    #ihvril_cnt=0
    #for item in log_files:
    #    if item.find("ihvril_")!=-1:
    #        ihvril_cnt = ihvril_cnt + 1
    #ihvril_cnt = log_files.count("ihvril_cnt")      
    print("ihvril_cnt = ", ihvril_cnt)
    if ihvril_cnt > 10:
        ihvril_delete_name = "ihvril_" + str(g_ihvril_del_index)
        print( "ihvril_delete_name = ",path_TelephonyTool+log_file[-1]+"\\"+ihvril_delete_name+".etl" )
        api_writefile( "ihvril_delete_name = "+path_TelephonyTool+log_file[-1]+"\\"+ihvril_delete_name+".etl" )
        os.popen( "del /S /Q "+path_TelephonyTool+log_file[-1]+"\\"+ihvril_delete_name+".etl"  )
        g_ihvril_del_index = g_ihvril_del_index + 1


    print("=============================")
    print("Start delete USBTrace log")
    UsbTrace_cnt=0
    #for item in log_files:
    #    if item.find("UsbTrace_")!=-1:
    #        UsbTrace_cnt = UsbTrace_cnt + 1
    #UsbTrace = log_files.count("UsbTrace_cnt")      
    print("UsbTrace_cnt = ", UsbTrace_cnt)
    if UsbTrace_cnt > 10:
        UsbTrace_delete_name = "UsbTrace_%06d"%g_UsbTrace_del_index
        print( "UsbTrace_delete_name = ",path_TelephonyTool+log_file[-1]+"\\"+UsbTrace_delete_name+".etl" )
        api_writefile( "UsbTrace_delete_name = "+path_TelephonyTool+log_file[-1]+"\\"+UsbTrace_delete_name+".etl" )
        os.popen( "del /S /Q "+path_TelephonyTool+log_file[-1]+"\\"+UsbTrace_delete_name+".etl"  )
        g_UsbTrace_del_index = g_UsbTrace_del_index + 1
        
        
    print("=============================")
    print("Start delete Modem log")
    #ModemTrace__cnt=0
    #for item in log_files:
    #    if item.find("ModemTrace_")!=-1:
    #        ModemTrace__cnt = ModemTrace__cnt + 1
    #UsbTrace = log_files.count("UsbTrace_cnt")      
    print("ModemTrace_cnt = ", ModemTrace_cnt)
    ModemTrace_ind=0
    for item in log_files:
        if item.find("ModemTrace_")!=-1:
            break
        ModemTrace_ind = ModemTrace_ind + 1
    print("ModemTrace_ind = ", ModemTrace_ind)
    print("ModemTrace_name = ", log_files[ModemTrace_ind])    
    if ModemTrace_cnt > 4:
        print( "ModemTrace_delete_name = "+path_TelephonyTool+log_file[-1]+"\\"+log_files[ModemTrace_ind+1] )
        #api_writefile( "ModemTrace_delete_name = "+path_TelephonyTool+log_file[-1]+"\\"+log_files[ModemTrace_ind+1]+".istp" )
        os.popen( "del /S /Q "+path_TelephonyTool+log_file[-1]+"\\"+log_files[ModemTrace_ind+1] )
    '''
    if ModemTrace__cnt > 2:
        ModemTrace_delete_name = "ModemTrace_%06d"%g_ModemTrace_del_index
        print( "UsbTrace_delete_name = ",path_TelephonyTool+log_file[-1]+"\\"+UsbTrace_delete_name+".etl" )
        api_writefile( "UsbTrace_delete_name = "+path_TelephonyTool+log_file[-1]+"\\"+UsbTrace_delete_name+".etl" )
        os.popen( "del /S /Q "+path_TelephonyTool+log_file[-1]+"\\"+UsbTrace_delete_name+".etl"  )
        g_UsbTrace_del_index = g_UsbTrace_del_index + 1       
'''        

    '''
    print("delete MODEM log")
    #delete MODEM log
    ModemTrace_cnt=0
    for item in log_files:
        if item.find("ModemTrace_")!=-1:
            ModemTrace_cnt = ModemTrace_cnt + 1
    if ModemTrace_cnt > 1:
        for item in log_files:
            if item.find("ModemTrace_")!=-1:
                print("ModemTrace_ = ",path_TelephonyTool+log_file[-1]+"\\"+item )
                #os.popen( "del /S /Q "+path_TelephonyTool+log_file[-1]+"\\"+item )
                #return
     ''' 




def Timer_Process():
    print("Timer_Process: "+(str( time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) )+"\n\n"))
    delete_log_resume()
    Timer_Start()
    
def Timer_Start(timeout=20):
    global g_Timer
    g_Timer = threading.Timer(timeout, Timer_Process)
    g_Timer.start()

def Timer_Stop():
    global g_Timer
    g_Timer.cancel()


g_DeviceCheck_while=1
g_Ping_while=1

g_DeviceCheck_flag=1
g_Ping_flag=1
g_DeleteLog_flag=1


g_Ping_times=1

g_TelephonyTool_Path="c:\\users\\fibocom\\documents\\intel\\telephonytool\\trace_folder\\"

if __name__ == "__main__":
    g_CurrentPath=os.getcwd()
    path = g_CurrentPath+"\\delete_log.txt"

    
    if g_DeleteLog_flag==1 :
        Timer_Process()
    
    call_S3()
    
    
    
    
        
        

