@Echo Off
Title ip1�ƶ˸��� Xray ��������
cd /d %~dp0
..\..\wget -t 2 --no-check-certificate https://www.gitlabip.xyz/Alvin9999/pac2/master/xray/1/config.json

if exist config.json goto startcopy

..\..\wget -t 2 --no-check-certificate https://gitlab.com/free9999/ipupdate/-/raw/master/xray/config.json

if exist config.json goto startcopy

echo ip����ʧ�ܣ�����������ip����
pause
exit
:startcopy

del "..\config.json_backup"
ren "..\config.json"  config.json_backup
copy /y "%~dp0config.json" ..\config.json
del "%~dp0config.json"
ECHO.&ECHO.�Ѹ����������Xray����,�밴�س�����ո���������� &PAUSE >NUL 2>NUL
exit