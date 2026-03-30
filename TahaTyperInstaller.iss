; TahaTyper Installer Script for Inno Setup
; To use this: Install Inno Setup (https://jrsoftware.org/isdl.php), open this file, and click Compile.

[Setup]
AppName=TahaTyper
AppVersion=1.0
DefaultDirName={pf}\TahaTyper
DefaultGroupName=TahaTyper
UninstallDisplayIcon={app}\TahaTyper.exe
Compression=lzma2
SolidCompression=yes
OutputDir=dist
OutputBaseFilename=TahaTyper_Setup
SetupIconFile=TahaTyper.ico

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; IMPORTANT: This assumes TahaTyper.exe is in the "dist" folder created by PyInstaller
Source: "dist\TahaTyper.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\TahaTyper"; Filename: "{app}\TahaTyper.exe"
Name: "{commondesktop}\TahaTyper"; Filename: "{app}\TahaTyper.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\TahaTyper.exe"; Description: "{cm:LaunchProgram,TahaTyper}"; Flags: nowait postinstall skipifsilent
