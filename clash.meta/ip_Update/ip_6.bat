@Echo Off
Title ip2�ƶ˸��� clash ��������
cd /d %~dp0
..\..\wget -t 2 --no-check-certificate https://www.githubip.xyz/Alvin9999/pac2/master/clash.meta2/3/config.yaml

if exist config.yaml goto startcopy

..\..\wget -t 2 --no-check-certificate https://fastly.jsdelivr.net/gh/Alvin9999/pac2@latest/clash.meta2/3/config.yaml

if exist config.yaml goto startcopy

echo ip����ʧ�ܣ�����������ip����


pause
exit
:startcopy

del "..\config.yaml_backup"
ren "..\config.yaml"  config.yaml_backup
copy /y "%~dp0config.yaml" ..\config.yaml
del "%~dp0config.yaml"
ECHO.&ECHO.�Ѹ����������clash.meta����,�밴�س�����ո���������� &PAUSE >NUL 2>NUL
exit