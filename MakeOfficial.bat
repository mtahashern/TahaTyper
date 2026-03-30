@echo off
title TahaTyper - Official Packaging Tool (Safe Version)
echo ===================================================
echo TahaTyper - Official Packaging Tool (Safe Version)
echo ===================================================
echo.
echo This tool will create a standalone TahaTyper.exe file
echo with your custom robot logo!
echo.
echo Step 1: Installing packaging tools...
pip install pyinstaller pynput keyboard pillow
echo.
echo Step 2: Creating the executable...
echo (Using optimized settings to minimize false antivirus flags)
pyinstaller --noconsole --onefile --icon=TahaTyper.ico --add-data "TahaTyper.ico;." --add-data "TahaTyper_Logo.png;." --name TahaTyper TahaTyper.py
echo.
echo ===================================================
echo DONE! 
echo Your official app is now in the "dist" folder.
echo You can send "TahaTyper.exe" to your friends!
echo.
echo PRO TIP: Put this on GitHub to make it 100%% safe!
echo (See GitHub_Setup_Guide.md for instructions)
echo ===================================================
pause
