@echo off

:: @==========================Install required packages=============================@ ::
echo "Installing required packages..."
pip install -r requirements.txt

echo "Done installing..."

:: @==========================Run our python script=============================@ ::
set path=%~dp0

set absolute=%path%main.py
echo Found main.py path %absolute%

"C:\Python310\python.exe" %absolute%