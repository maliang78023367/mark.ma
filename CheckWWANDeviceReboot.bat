@echo off
set /a times=0

for /f "delims=" %%a in (times.txt) do (
	set /a times=%%a
)

set /a times=%times%+1

setlocal enabledelayedexpansion
for /L %%i in (1,1,20) do (
	ping 127.0.0.1
	CheckWWANDevice.exe  "VEN_8086&DEV_7560"	
	if !errorlevel!==0 (
		echo ok > times.txt

	) else (
		echo Can not Find The WWAN PCI Device!!!
	)
)

if !errorlevel! neq 0 (
echo Can not Find The WWAN PCI Device after 1 minute!!!
pause
)