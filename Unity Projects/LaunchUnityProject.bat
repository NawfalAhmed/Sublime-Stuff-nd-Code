@ECHO off
set selectedproj=%1
set selectedproj=%selectedproj:"=%
cd %USERPROFILE%
del "AppData\Roaming\Unity\Editor-5.x\Preferences\Layouts\default\default.wlt"
del "AppData\Roaming\Unity\Editor-5.x\Preferences\Layouts\default\LastLayout.dwlt"
del "Desktop\Unity Projects\%selectedproj%\Library\CurrentLayout-default.dwlt"
cd "C:\Program Files\Unity\Hub\Editor\2020.1.6f1\Editor\"
Unity.exe -projectPath "%USERPROFILE%\Desktop\Unity Projects\%selectedproj%"
