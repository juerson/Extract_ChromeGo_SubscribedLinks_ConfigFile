@Echo Off
Title ip2云端更新 v2free 最新配置
cd /d %~dp0
..\..\wget -t 5 --no-check-certificate https://www.githubip.xyz/jsvpn/jsproxy/dev/yule/20200325/1299699.md

if exist 1299699.md goto startcopy
echo ip更新失败，请试试ip_2更新
pause
exit
:startcopy

del "..\v2free.json_backup"
ren "..\v2free.json"  v2free.json_backup
copy /y "%~dp01299699.md" ..\v2free.json
del "%~dp01299699.md"
ECHO.&ECHO.已更新完成最新v2free配置,请按回车键或空格键启动程序！ &PAUSE >NUL 2>NUL
exit