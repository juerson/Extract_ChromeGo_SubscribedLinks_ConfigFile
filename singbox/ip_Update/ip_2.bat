@Echo Off
Title ip2�ƶ˸��� singbox ��������
cd /d %~dp0
..\..\wget -t 2 --no-check-certificate https://www.githubip.xyz/Alvin9999/pac2/master/singbox/config.json

if exist config.json goto startcopy

..\..\wget -t 2 --no-check-certificate https://fastly.jsdelivr.net/gh/Alvin9999/pac2@latest/singbox/config.json

if exist config.json goto startcopy

echo ip����ʧ�ܣ�������ip_2����
pause
exit
:startcopy

del "..\config.json_backup"
ren "..\config.json"  config.json_backup
copy /y "%~dp0config.json" ..\config.json
del "%~dp0config.json"
ECHO.&ECHO.�Ѹ����������singbox����,�밴�س�����ո���������� &PAUSE >NUL 2>NUL
exit