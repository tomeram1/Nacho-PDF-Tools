@echo off
chcp 65001 >nul

:: Use LocalAppData folder instead of C drive to prevent permission errors
set "AppDir=%LOCALAPPDATA%\Nacho_pdf_help"
if not exist "%AppDir%" mkdir "%AppDir%"
copy /y "%~dp0Nacho_pdf_help.exe" "%AppDir%\Nacho_pdf_help.exe" >nul

set "SendToDir=%APPDATA%\Microsoft\Windows\SendTo"
set "ShortcutPath=%SendToDir%\Nacho PDF Help.lnk"

:: Create the shortcut
powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%ShortcutPath%'); $Shortcut.TargetPath = '%AppDir%\Nacho_pdf_help.exe'; $Shortcut.Save()"

:: Completion message
powershell.exe -NoProfile -WindowStyle Hidden -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('Nacho PDF Help Installation Has finished', 'Nacho PDF Help Installer', 0, 64)"