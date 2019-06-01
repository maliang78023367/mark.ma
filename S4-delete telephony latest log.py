import sys,os,re,time
import subprocess as sp
import win32api,win32con,winreg


g_Restart_Cnt=0
g_CurrentPath=''
g_Ping_Times=3
g_Resume_S3_times=3
g_Resume_S4_times=3





####################################################
def check_restart():
    api_writefile( "==============================================" )
    api_writefile( "==============================================" )
    api_writefile( "================= START ======================" )
    api_writefile(str( time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) )+"\n\n")
    
    log_name = str( time.strftime('%Y-%m-%d_%H_%M_%S',time.localtime(time.time())) )
    print(log_name)

####################################################
def api_writefile(ss=''):
    
    # log file path
    path = g_CurrentPath+"\\log.txt"
    
    
    
    
    with open(path,'a') as log_file:	
        log_file.write(ss+'\n')
        print(ss)


####################################################
def check_device():

    #============================
    # check HWID
    #print( os.popen("cd Python36\test") )
    #p=os.popen("cd \\ &&cd python36\\restart && check_hwid.bat")
    cmd = "cd \\ &&cd " +g_CurrentPath+ " && check_hwid.bat"
    p=os.popen(cmd)
    time.sleep(2)#wait 2s
    path = g_CurrentPath + "\\check_hwid.log"
    with open(path,'r') as check_hwid:
        str_check_hwid=check_hwid.read()
    
        if str_check_hwid.find("PCIe-OK")!=-1:
            api_writefile("====== " +__file__+ " PCIe SUCCESS ======\n")
        else:
            api_writefile("====== " +__file__+ " PCIe FAIL ======\n")
    
        if str_check_hwid.find("ModemCtl-OK")!=-1:
            api_writefile("====== " +__file__+ " ModemCtl SUCCESS ======\n")
        else:	
            api_writefile("====== " +__file__+ " ModemCtl FAIL ======\n")
            
        if str_check_hwid.find("MBIM-OK")!=-1:
            api_writefile("====== " +__file__+ " MBIM SUCCESS ======\n")
        else:
            api_writefile("====== " +__file__+ " MBIM FAIL ======\n")


####################################################
def check_ping(times=g_Ping_Times):

    cmd_Ping="@ping -n 10 www.baidu.com"
    cmd_DeviceInfo="netsh mbn show interfaces"
    cnt=0
    
    popen("netsh wlan disconnect")
    for i in range(0,times):
        time.sleep(40)
        
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
        if (str_return.find("(100% loss)"))==-1 :
            api_writefile("====== " +__file__+ " PING SUCCESS ======\n")
            break;
        else:
            cnt = cnt + 1
            
    if cnt>=times:
        api_writefile("====== " +__file__+ " PING Fail ======\n")


####################################################
def call_S4(           Total                = g_Resume_S4_times, # resume  times
                    w_time_after_resume  = 50,
                    Ping_Check           = 30,
                    BreakAftError        = 1,
                    SleepTime            = 60
                    ):
        api_writefile("\n\n" + "*"*50)
        api_writefile(str( time.ctime(time.time()) ))
        api_writefile("\nCall S4: S4 cycles  = " + str(Total))
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
        hibernate = path + "\\Tool\\pwrtest.exe /sleep /c:1 /s:4 /d:30 /p:%s" % str(SleepTime)
        for i in range (0,Total):
            cycle_number = str(i+1) + str('/') + str(Total)
            api_writefile("\n"+"-"*50)
            api_writefile("Entering into S4 cycle: " + cycle_number)
            
            time.sleep(3) #Wait 3 seconds to see the printing log
            
            start = time.clock()
            process = sp.Popen(hibernate, shell = True, stdout = sp.PIPE, stderr = sp.PIPE)
            (output, err) = process.communicate()
            
            elasped = (time.clock()-start)
            api_writefile(str("Exited the S4 cycle: ") + str(i+1))
            api_writefile(str("Approx time into S4 state: ") + str(elasped))
            fail_count=i+1                
    
            time.sleep(w_time_after_resume) #adding the wait time for the system to resume from the sleep state.
            
            
            #win32api.keybd_event(37,0,0,0)
            #win32api.keybd_event(37,0,win32con.KEYEVENTF_KEYUP,0)
    
            #here check the MBIM Status
            check_ping()                    
            time.sleep(2)
            
            if i == Total:
                api_writefile("\n[Success]:\nThe S4 test has completed sucessfully")
                return 1


####################################################
def call_S3(           Total                = g_Resume_S3_times, # resume  times
                    w_time_after_resume  = 50,
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
        check_ping()                    
        time.sleep(2)
        
        if i == Total:
            api_writefile("\n[Success]:\nThe S3 test has completed sucessfully")
            return 1
    

def do_something():	
    print( "do_something" )
    
    cmd_CellularName=" \"Cellular 2 \" "
    cmd_DeviceInfo="netsh mbn show interfaces"
    cmd_CellularOn="netsh mbn set powerstate interface="+cmd_CellularName+ " on"
    cmd_CellularOff="netsh mbn set powerstate interface="+cmd_CellularName+" off"
    
    cmd_Disconnect="netsh mbn set acstate interface="+cmd_CellularName+" state=autooff"
    cmd_Connect="netsh mbn set acstate interface="+cmd_CellularName+" state=autoon"
    
    cmd_Ping="@ping -n 10 www.baidu.com"
    cmd_dir="dir"
    
    #with open(os.path.dirname(os.path.realpath(__file__))+"\log.txt",'a') as file1:
    with open("c:\\Python36\\restart\\restart_log.txt",'a') as log_file:
        time.sleep(3)#wait 3s
        log_file.write("==============================================\n")
        log_file.write("=================== START ====================\n")
        print(str( time.ctime(time.time()) ))
        #############################
        #============================
        # check HWID
        #print( os.popen("cd Python36\test") )
        p=os.popen("cd \\ &&cd python36\\restart && check_hwid.bat")
        #p=os.popen("runas /user:administrator "c:\\python\\test\\devcon.exe hwids *>hwid.log" ")
        time.sleep(2)#wait 2s
        with open("c:\\Python36\\restart\\check_hwid.log",'r') as check_hwid:
            str_check_hwid=check_hwid.read()
    
            if str_check_hwid.find("PCIe-OK")!=-1:
                log_file.write("====== RESTART PCIe SUCCESS ======\n")
                print("====== RESTART PCIe SUCCESS ======\n")
            else:
                log_file.write("====== RESTART PCIe FAIL ======\n")
                print("====== RESTART PCIe FAIL ======\n")		
                
            if str_check_hwid.find("ModemCtl-OK")!=-1:
                log_file.write("====== RESTART ModemCtl SUCCESS ======\n")
                print("====== RESTART ModemCtl SUCCESS ======\n")
            else:
                log_file.write("====== RESTART ModemCtl FAIL ======\n")
                print("====== RESTART ModemCtl FAIL ======\n")		
                
            if str_check_hwid.find("MBIM-OK")!=-1:
                log_file.write("====== RESTART MBIM SUCCESS ======\n")
                print("====== RESTART MBIM SUCCESS ======\n")
            else:
                log_file.write("====== RESTART MBIM FAIL ======\n")
                print("====== RESTART MBIM FAIL ======\n")	
        ############################
        
        
        
        
    with open("c:\\Python36\\restart\\restart_log.txt",'a') as log_file:	
        p=os.popen(cmd_DeviceInfo)
        str_return=p.read()
        log_file.write(str_return)
        #====================================
        # Interface Name
        #interfaces=str_return[(str_return.find(":",86)+2):(str_return.find("\n",86))]
        
        #====================================
        # Check Attach status		
        #if str_return.find("Connected",1)==-1:
        #	log_file.write("====== CONNECT FAIL ======\n")
        #	print("====== CONNECT FAIL ======\n")
        
        #====================================
        # Cellular Off		
        #p=os.popen(cmd_CellularOff)
        #time.sleep(5)
    
        #====================================
        # Cellular On		
        #p=os.popen(cmd_CellularOn)
        time.sleep(50)		
    
    with open("c:\\Python36\\restart\\restart_log.txt",'a') as log_file:	
        #====================================
        # Ping		
        p=os.popen(cmd_Ping)
        str_return=p.read()
        log_file.write(str_return)	
        if (str_return.find("(100% loss)"))==-1 :
            log_file.write("====== RESTART PING SUCCESS ======\n")
            print("======= RESTART PING SUCCESS ======\n")
        else:
            log_file.write("====== RESTART PING FAIL ======\n")
            print("======= RESTART PING FAIL ======\n")	

            
####################################################
if __name__ == "__main__":
    #print( sys.argv[0] 
    
    
    g_CurrentPath=os.getcwd()
    path = g_CurrentPath+"\\delete_log.txt"
    
    try:
        with open(path,'r') as log_file:
            f_str=log_file.read() 

            print("\n\n\n==========")
            print( f_str )  
            print( path )
            print("===== delete =====")
            os.popen( "rd /S /Q "+path )     
            os.popen( "rd /S /Q "+f_str )  
            print("==========\n\n\n")
    except:
        pass
'''
    time.sleep(3)#wait 2s
    for root,dirs,files in os.walk( "C:\\Users\\GodzillaB13\\Documents\\Intel\\TelephonyTool\\trace_folder" ):
        print("root", root)
        #print("dirs", dirs)
        #print("files", files)
        
    # log file path
    path = g_CurrentPath+"\\delete_log.txt"

    with open(path,'w+') as log_file:
        log_file.write(root+'\n')   # no error log
    print(root+'\n')# no error log
'''





	