@ECHO OFF
PATH C:\FREEDOS\BIN;C:\;C:\DOSEMU;H:\
PROMPT $P$G
SHSUCDX /D:MSCD0001
SET DOSDIR=""
SET HELPPATH=C:\FREEDOS\HELP\

UNIX -s DOSDIR
IF %DOSDIR% == "" GOTO END
LREDIR H: LINUX\FS%DOSDIR%
:: allow user customization
IF EXIST H:\AUTOEXEC.BAT H:\AUTOEXEC.BAT

:END
