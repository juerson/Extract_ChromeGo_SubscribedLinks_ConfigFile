@Echo Off
Title ip2云端更新 Xray 最新配置
cd /d %~dp0
..\..\wget -t 2 --no-check-certificate https://www.githubip.xyz/Alvin9999/pac2/master/xray/config.json

if exist config.json goto startcopy

..\..\wget -t 2 --no-check-certificate https://fastly.jsdelivr.net/gh/Alvin9999/pac2@latest/xray/config.json

if exist config.json goto startcopy

echo ip更新失败，请试试其它ip更新
pause
exit
:startcopy

del "..\config.json_backup"
ren "..\config.json"  config.json_backup
copy /y "%~dp0config.json" ..\config.json
del "%~dp0config.json"
ECHO.&ECHO.已更新完成最新Xray配置,请按回车键或空格键启动程序！ &PAUSE >NUL 2>NUL
exit