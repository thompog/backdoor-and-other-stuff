import os, sys, subprocess

try:
    import requests
except ModuleNotFoundError:
    subprocess.run("python -m pip isntall requests")

def github_get_filename(url):
    return url.split("/")[-1]

def install(url=""):
    """enter a url to download from that url or enter a python module to install that"""
    if url.startwith("https://www.") or url.startswith("https://raw."):
        respones = requests.get(url)
        respones.raise_for_status()

        filename = github_get_filename(url)

        with open(f"{filename}", "w") as f:
            f.write(respones.text)
    else:
        subprocess.run(f"python -m pip install {url}")

