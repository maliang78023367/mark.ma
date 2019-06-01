@echo off


setlocal enabledelayedexpansion

CheckWWANDevice.exe  "VEN_8086&DEV_7560"	

if !errorlevel!==0 (
	echo PCIe-OK > check_hwid.log
) else (
	echo Can not Find The WWAN PCI Device!!! > check_hwid.log
)



CheckWWANDevice.exe  "USB\VID_8087&PID_0ADA"
	
if !errorlevel!==0 (
	echo ModemCtl-OK >> check_hwid.log
) else (
	echo Can not Find The WWAN ModemCtl Device!!! > check_hwid.log
)



CheckWWANDevice.exe  "USB\VID_8087&PID_0AC9"

if !errorlevel!==0 (
	echo MBIM-OK >> check_hwid.log
) else (
	echo Can not Find The WWAN MBIM Device!!! > check_hwid.log
)