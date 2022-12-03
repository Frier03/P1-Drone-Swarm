@echo off

:: @==========================Install required packages=============================@ ::
ECHO "Installing required packages..."
CALL pip install -r requirements.txt
IF errorlevel 1 GOTO ERROR
ECHO Successfully installed all packages located inside requirements.txt
GOTO PS

:: @==========================Run our python script=============================@ ::
:PS
set path=%~dp0

set absolute=%path%main.py
echo Found main.py path %absolute%

"C:\Python310\python.exe" %absolute%


:: @==========================Error Handling=============================@ ::
:ERROR
ECHO Locating the error...
for /F "" %%x in (requirements.txt) do (
    echo %%x|find "#" >nul
    if errorlevel 1 (
        timeout /T 1 /NOBREAK
        echo Package file   %%x

        SET str = pygame
        if %%x == %str% (
            :: Try to download the fixed version of pygame
            ECHO pip install pygame
            if errorlevel 1 (
                ECHO Found an issue when trying to install pygame 
                ECHO Trying to fix the issue...
                CALL pip install pygame --pre
                if errorlevel1 (
                    ECHO Cannot fix the issue.
                    timeout /T 1 /NOBREAK
                ) else (
                    ECHO Fixed the issue and successfully installed pygame
                    timeout /T 1 /NOBREAK
                )
            )
        )
    ) 
)
