@Echo Off
Title ip1�ƶ˸��� hysteria ��������
cd /d %~dp0
..\..\wget -t 2 --no-check-certificate https://www.gitlabip.xyz/Alvin9999/PAC/master/naiveproxy/1/config.json
if exist config.json goto startcopy

..\..\wget -t 2 --no-check-certificate https://gitlab.com/free9999/ipupdate/-/raw/master/naiveproxy/config.json

if exist config.json goto startcopy

echo ip����ʧ�ܣ�������ip_2����
pause
exit
:startcopy

del "..\config.json_backup"
ren "..\config.json"  config.json_backup
copy /y "%~dp0config.json" ..\config.json
del "%~dp0config.json"
ECHO.&ECHO.�Ѹ����������naiveproxy����,�밴�س�����ո���������� &PAUSE >NUL 2>NUL
exit