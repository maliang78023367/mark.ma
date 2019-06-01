import sys,os,re,time
import subprocess as sp
import _thread
import ctypes
import subprocess as sp


g_Restart_Cnt=0
g_CurrentPath=''
g_Ping_Times=3
g_Resume_S3_times=2
g_Resume_S4_times=2
g_Err_cnt=0
g_Flag_Suspend=0




####################################################
def check_restart():
    api_writefile( "\n\n\n==============================================" )
    api_writefile( "==============================================" )
    api_writefile( "================= START ======================" )
    api_writefile(str( time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) )+"\n\n")
    
    #log_name = str( time.strftime('%Y-%m-%d_%H_%M_%S',time.localtime(time.time())) )
    #print(log_name)

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

    
        if str_check_hwid.find("ModemCtl-OK")!=-1:
            api_writefile("====== " +out+ " ModemCtl SUCCESS ======\n")
        else:	
            api_writefile("====== " +out+ " ModemCtl FAIL ======\n")

            
        if str_check_hwid.find("MBIM-OK")!=-1:
            api_writefile("====== " +out+ " MBIM SUCCESS ======\n")
        else:
            api_writefile("====== " +out+ " MBIM FAIL ======\n")

                    
        #p=os.popen("cd \\ &&cd python36\\restart && check_hwid.bat")
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
                

    #os.popen("del "+ path)
    #path = g_CurrentPath + "\\devcon.log"
    #os.popen("del "+ path)


    
####################################################
def check_ping(times=12, out=""):
    player = ctypes.windll.kernel32
    cmd_Ping="@ping -n 10 www.baidu.com"
    cmd_DeviceInfo="netsh mbn show interfaces"
    cnt=0
    
    #os.popen("netsh wlan disconnect")
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
        #while(1):
        #    time.sleep(1)
        #    player.Beep(1000,300)
        return
    
    find_TelephonyTool_log()



"""
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
"""				



def do_usercase():
    check_restart()
    #check_device(out="restart")
    time.sleep(15)
    #check_ping(out="restart") 
    call_S4(Total=5)
    check_end()    

    
def find_TelephonyTool_log():
    CurrentPath=os.getcwd()
    path_TelephonyTool="C:\\Users\\wwan-hw\\Documents\\Intel\\TelephonyTool\\trace_folder\\"

    #for root,dirs,files in os.walk(path_TelephonyTool):
    #    log_file = root
        #print(root)
    log_file = os.listdir(path_TelephonyTool)
    print(log_file)
    print("log folder =",len(log_file))
    # do not delete log if capture coredump file.
    log_files = os.listdir(path_TelephonyTool+log_file[-1])
    print( log_files )

    for item in log_files:
        if item.find("COREDUMP")!=-1:
            print("+++ find_TelephonyTool_log COREDUMP +++")
            return

    path = CurrentPath+"\\delete_telephonylog.txt"
    print("+++ find_TelephonyTool_log +++")
    with open(path,'a') as delte_log:
        delte_log.write(path_TelephonyTool+log_file[-1]+'\n')
        print(path_TelephonyTool+log_file[-1])

def delete_TelephonyTool_log():
    CurrentPath=os.getcwd()
    path = CurrentPath+"\\delete_telephonylog.txt"

    try:
        with open(path,'r+') as log_file:
            f_str=log_file.read() 

            print("\n\n\n==========")
            print( f_str )  
            print( path )
            print("===== delete =====")
            os.popen( "rd /S /Q "+f_str )
            #os.popen( "rd /S /Q "+path )
            print("==========\n\n\n")
            #log_file.truncate()
    except:
        pass
        
    # remove delete_telephonylog.txt
    try:   
        os.remove(path)
        pass
    except:
        pass
####################################################
if __name__ == "__main__":
    #print( sys.argv[0] )
    
    time.sleep(1)
    path_TelephonyTool="C:\\Users\\wwan-hw\\Documents\\Intel\\TelephonyTool\\trace_folder\\"
    log_file = os.listdir(path_TelephonyTool)
    print(log_file)
    print("log folder =",len(log_file))
    if( len(log_file)>4 ):
        del_dir=log_file[0]
        print(path_TelephonyTool+log_file[1])
        os.popen( "rd /S /Q "+path_TelephonyTool+log_file[1] )


    
    
    
    
    
    
    
    
    
