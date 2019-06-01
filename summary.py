test for dev branch:wq

import sys,os,re,time











def summary( ss='' ):
    path=os.getcwd()+"\\summary.txt"
    with open(path,'a') as log_file:
        log_file.write(ss)

def check_restart(ss):

    restart_cnt=0
    restart_pcie_cnt=0
    restart_modem_cnt=0
    restart_mbim_cnt=0
    restart_fw_cnt=0
    restart_ping_cnt=0
    restart_end_cnt=0
    
    if line.find( "================= START ======================" )!=-1:
        restart_cnt+=1

        
        
    elif line.find( "====== restart PCIe SUCCESS ======" )!=-1:
        restart_pcie_cnt+=1
    elif line.find( "====== restart PCIe FAIL ======" )!=-1:
        summary("====== restart PCIe FAIL ======"+">>>>>> ERR = "+line_cnt)
        
        
    elif line.find( "====== restart ModemCtl SUCCESS ======" )!=-1:
        restart_modem_cnt+=1
    elif line.find( "====== restart ModemCtl FAIL ======" )!=-1:
        summary("====== restart ModemCtl FAIL ======"+">>>>>> ERR = "+line_cnt)
        
        
    elif line.find( "====== restart MBIM SUCCESS ======" )!=-1:
        restart_mbim_cnt+=1
    elif line.find( "====== restart MBIM FAIL ======" )!=-1:
        summary("====== restart MBIM FAIL ======"+">>>>>> ERR = "+line_cnt)
        
        
    elif line.find( "====== restart FWUpdateDriver SUCCESS ======" )!=-1:
        restart_fw_cnt+=1
    elif line.find( "====== restart FWUpdateDriver FAIL ======" )!=-1:
        summary("====== restart FWUpdateDriver FAIL ======"+">>>>>> ERR = "+line_cnt)
        
        
    elif line.find( "====== restart PING SUCCESS ======" )!=-1:
        restart_ping_cnt+=1
    elif line.find( "====== restart PING FAIL ======" )!=-1:
        summary("====== restart PING FAIL ======"+">>>>>> ERR = "+line_cnt)

        
        
    elif line.find( "=================== END ======================" )!=-1:
        restart_end_cnt+=1
        
    return restart_cnt, restart_pcie_cnt,restart_modem_cnt,restart_mbim_cnt,restart_fw_cnt,restart_ping_cnt,restart_end_cnt
        

def summary_restart():
    summary("\n================= START ======================"+"        >>>>>>"+restart_cnt)
    summary("\n====== restart PCIe SUCCESS ======"+"                    >>>>>>"+restart_pcie_cnt)
    summary("\n====== restart ModemCtl SUCCESS ======"+"                >>>>>>"+restart_modem_cnt)
    summary("\n====== restart MBIM SUCCESS ======"+"                    >>>>>>"+restart_mbim_cnt)
    summary("\n====== restart FWUpdateDriver SUCCESS ======"+"          >>>>>>"+restart_fw_cnt)
    summary("\n====== restart PING SUCCESS ======"+"                    >>>>>>"+restart_ping_cnt)
        
        

if __name__ == "__main__":
    
    g_CurrentPath=os.getcwd()
    path = g_CurrentPath+"\\log.txt"
    
    restart_cnt=0
    restart_pcie_cnt=0
    restart_modem_cnt=0
    restart_mbim_cnt=0
    restart_fw_cnt=0
    restart_ping_cnt=0
    manual_connect_cnt=0
    restart_end_cnt=0
    line_cnt=0

    
    s4_pcie_cnt=0
    s4_modem_cnt=0
    s4_mbim_cnt=0
    s4_fw_cnt=0
    s4_ping_cnt=0
    s4_end_cnt=0
    
    
    with open(path,'r') as log_file:
    
        line = log_file.readline() 
        line_cnt+=1
        while line:
            #print(line)

            if line.find( "================= START ======================" )!=-1:
                restart_cnt+=1

                
##################################################################################
##################################################################################
##################################################################################
            elif line.find( "====== restart PCIe SUCCESS ======" )!=-1:
                restart_pcie_cnt+=1
            elif line.find( "====== restart PCIe FAIL ======" )!=-1:
                summary("\n====== restart PCIe FAIL ======"+">>>>>> ERR = "+str( line_cnt) )
                
                
            elif line.find( "====== restart ModemCtl SUCCESS ======" )!=-1:
                restart_modem_cnt+=1
            elif line.find( "====== restart ModemCtl FAIL ======" )!=-1:
                summary("\n====== restart ModemCtl FAIL ======"+">>>>>> ERR = "+str( line_cnt) )
                
                
            elif line.find( "====== restart MBIM SUCCESS ======" )!=-1:
                restart_mbim_cnt+=1
            elif line.find( "====== restart MBIM FAIL ======" )!=-1:
                summary("\n====== restart MBIM FAIL ======"+">>>>>> ERR = "+str( line_cnt) )
                
                
            elif line.find( "====== restart FWUpdateDriver SUCCESS ======" )!=-1:
                restart_fw_cnt+=1
            elif line.find( "====== restart FWUpdateDriver FAIL ======" )!=-1:
                summary("\n====== restart FWUpdateDriver FAIL ======"+">>>>>> ERR = "+str( line_cnt) )
                
                
            elif line.find( "====== restart PING SUCCESS ======" )!=-1:
                restart_ping_cnt+=1
            elif line.find( "====== restart PING FAIL ======" )!=-1:
                summary("\n====== restart PING FAIL ======"+">>>>>> ERR = "+str( line_cnt) )
                
            elif line.find( "====== Manual Connect PING SUCCESS ======" )!=-1:
                manual_connect_cnt+=1
            elif line.find( "====== Manual Connect PING FAIL ======" )!=-1:
                summary("\n====== Manual Connect PING FAIL ======"+">>>>>> ERR = "+str( line_cnt) )
##################################################################################
##################################################################################
##################################################################################
            elif line.find( "====== S4 PCIe SUCCESS ======" )!=-1:
                s4_pcie_cnt+=1
            elif line.find( "====== S4 PCIe FAIL ======" )!=-1:
                summary("\n====== S4 PCIe FAIL ======"+">>>>>> ERR = "+str( line_cnt) )
                
                
            elif line.find( "====== S4 ModemCtl SUCCESS ======" )!=-1:
                s4_modem_cnt+=1
            elif line.find( "====== S4 ModemCtl FAIL ======" )!=-1:
                summary("\n====== S4 ModemCtl FAIL ======"+">>>>>> ERR = "+str( line_cnt) )
                
                
            elif line.find( "====== S4 MBIM SUCCESS ======" )!=-1:
                s4_mbim_cnt+=1
            elif line.find( "====== S4 MBIM FAIL ======" )!=-1:
                summary("\n====== S4 MBIM FAIL ======"+">>>>>> ERR = "+str( line_cnt) )
                
                
            elif line.find( "====== S4 FWUpdateDriver SUCCESS ======" )!=-1:
                s4_fw_cnt+=1
            elif line.find( "====== S4 FWUpdateDriver FAIL ======" )!=-1:
                summary("\n====== S4 FWUpdateDriver FAIL ======"+">>>>>> ERR = "+str( line_cnt) )
                
                
            elif line.find( "====== S4 PING SUCCESS ======" )!=-1:
                s4_ping_cnt+=1
            elif line.find( "====== S4 PING FAIL ======" )!=-1:
                summary("\n====== S4 PING FAIL ======"+">>>>>> ERR = "+str( line_cnt) )
                
##################################################################################
##################################################################################
##################################################################################
                
                
            elif line.find( "=================== END ======================" )!=-1:
                restart_end_cnt+=1

            
            line = log_file.readline()
            line_cnt+=1
        

    summary("\n\n\n\n\n================= START ======================"+"        >>>>>> "+str(restart_cnt) )
    summary("\n====== restart PCIe SUCCESS ======"+"                    >>>>>> "+str(restart_pcie_cnt) )
    summary("\n====== restart ModemCtl SUCCESS ======"+"                >>>>>> "+str(restart_modem_cnt) )
    summary("\n====== restart MBIM SUCCESS ======"+"                    >>>>>> "+str(restart_mbim_cnt) )
    summary("\n====== restart FWUpdateDriver SUCCESS ======"+"          >>>>>> "+str(restart_fw_cnt) )
    summary("\n====== restart PING SUCCESS ======"+"                    >>>>>> "+str(restart_ping_cnt) )
    summary("\n====== Manual Connect PING SUCCESS ======"+"             >>>>>> "+str(manual_connect_cnt) )
    
    summary("\n\n\n====== S4 PCIe SUCCESS ======"+"                    >>>>>> "+str(s4_pcie_cnt) )
    summary("\n====== S4 ModemCtl SUCCESS ======"+"                >>>>>> "+str(s4_modem_cnt) )
    summary("\n====== S4 MBIM SUCCESS ======"+"                    >>>>>> "+str(s4_mbim_cnt) )
    summary("\n====== S4 FWUpdateDriver SUCCESS ======"+"          >>>>>> "+str(s4_fw_cnt) )
    summary("\n====== S4 PING SUCCESS ======"+"                    >>>>>> "+str(s4_ping_cnt) )
    
    
    summary("\n================= END ======================"+"          >>>>>> "+str(restart_end_cnt) )
    
