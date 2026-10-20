@echo off
chcp 65001 >nul

:: מחיקת קיצור הדרך מתפריט שלח אל
set "SendToDir=%APPDATA%\Microsoft\Windows\SendTo"
set "ShortcutPath=%SendToDir%\Nacho PDF Help.lnk"
if exist "%ShortcutPath%" del "%ShortcutPath%"

:: מחיקת תיקיית התוכנה מ-LocalAppData
set "AppDir=%LOCALAPPDATA%\Nacho_pdf_help"
if exist "%AppDir%" rmdir /s /q "%AppDir%"

powershell.exe -NoProfile -WindowStyle Hidden -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('Nacho PDF Help Removal successful', 'Nacho PDF Help Removal', 0, 64)"