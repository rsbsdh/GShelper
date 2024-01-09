import win32com.shell.shell as shell
import sys
import win32com.client
import os
from pathlib import Path

def run_as_admin():

    script_path = os.path.abspath(__file__)
    
    shell_obj = win32com.client.Dispatch("WScript.Shell")
    
    shell_obj.Run(f'runas /noprofile /user:{os.environ["USERNAME"]} "{sys.executable}" "{script_path}"')

def modify_shortcut_target(shortcut_path):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    arguments = shortcut.Arguments
    new_arguments = f'{arguments} -popupwindow'
    shortcut.Arguments = new_arguments
    shortcut.Save()

desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
shortcut_path = os.path.join(desktop_path, 'YuanShen.exe - 快捷方式.lnk')

print(shortcut_path)
modify_shortcut_target(shortcut_path)


if not shell.IsUserAnAdmin():

    run_as_admin()
