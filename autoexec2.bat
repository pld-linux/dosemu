@ECHO OFF
PATH C:\FREEDOS\BIN;C:\;C:\DOSEMU;H:\
PROMPT $P$G
SHSUCDX /D:MSCD0001
SET DOSDIR=""
UNIX -s DOSDIR
IF %DOSDIR% == "" GOTO END
LREDIR H: LINUX\FS%DOSDIR%
:END
