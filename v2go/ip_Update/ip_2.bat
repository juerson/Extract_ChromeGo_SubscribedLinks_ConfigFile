@Echo Off
Title ip2�ƶ˸��� v2free ��������
cd /d %~dp0
..\..\wget -t 5 --no-check-certificate https://www.githubip.xyz/jsvpn/jsproxy/dev/yule/20200325/1299699.md

if exist 1299699.md goto startcopy
echo ip����ʧ�ܣ�������ip_2����
pause
exit
:startcopy

del "..\v2free.json_backup"
ren "..\v2free.json"  v2free.json_backup
copy /y "%~dp01299699.md" ..\v2free.json
del "%~dp01299699.md"
ECHO.&ECHO.�Ѹ����������v2free����,�밴�س�����ո���������� &PAUSE >NUL 2>NUL
exit