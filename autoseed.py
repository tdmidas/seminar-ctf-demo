# -*- coding: utf-8 -*-
# Tu dong seed 2 challenge khi container khoi dong (chi khi CTFd con moi tinh).
import os
import sys
import time
import subprocess
import urllib.request

BASE = "http://127.0.0.1:8000"
EMAIL = os.environ.get("ADMIN_EMAIL", "admin@uit.edu.vn")
PASSW = os.environ.get("ADMIN_PASSWORD", "AdminUIT@2026")
SEED = "/opt/seed/seed_ctfd.py"


def reachable():
    try:
        urllib.request.urlopen(BASE + "/", timeout=3)
        return True
    except Exception:
        return False


def already_setup():
    # /setup cua CTFd da setup roi se redirect ve "/" -> khong con ket thuc bang /setup
    try:
        r = urllib.request.urlopen(BASE + "/setup", timeout=5)
        return not r.geturl().rstrip("/").endswith("/setup")
    except Exception:
        return False


def main():
    # 1) doi CTFd len (toi da ~120s)
    for _ in range(60):
        if reachable():
            break
        time.sleep(2)
    else:
        print("[autoseed] CTFd khong phan hoi -> bo qua seed", flush=True)
        return

    # 2) chi seed khi con moi (tranh ghi de diem khi dung DB lau dai)
    if already_setup():
        print("[autoseed] CTFd da setup tu truoc -> bo qua seed", flush=True)
        return

    # 3) chay seeder da test (tu /setup + tao 2 cau + upload file)
    print("[autoseed] Bat dau seed 2 challenge...", flush=True)
    subprocess.run([sys.executable, SEED, BASE, "admin", EMAIL, PASSW])
    print("[autoseed] Xong.", flush=True)


if __name__ == "__main__":
    main()
