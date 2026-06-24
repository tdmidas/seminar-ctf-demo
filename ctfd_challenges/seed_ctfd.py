#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
seed_ctfd.py  --  Tu dong TICH HOP 3 challenge vao 1 CTFd dang chay.
============================================================================
Script nay se:
  1. Chay buoc /setup (tao tai khoan admin + ten CTF) neu CTFd con moi tinh.
  2. Dong bo 2 challenge (Cau 2 + Cau 3): xoa ban cu cung ten roi tao lai cho
     dung mo ta / hint / flag / file moi nhat. Tu dong XOA "Cau 1" cu neu con.

YEU CAU: CTFd da chay (vd: docker compose up, hoac docker run ctfd/ctfd),
         va  pip install requests  (thuong co san).

CACH CHAY:
    python seed_ctfd.py                       # mac dinh http://localhost:8000
    python seed_ctfd.py http://localhost:8000 admin admin@uit.edu.vn MatKhauManh123
Tham so: <BASE_URL> <admin_user> <admin_email> <admin_password>
============================================================================
"""
import os
import re
import sys
import requests

# In tieng Viet ra console khong bi loi 'charmap' (Windows)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

BASE  = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
ADMIN = sys.argv[2] if len(sys.argv) > 2 else "admin"
EMAIL = sys.argv[3] if len(sys.argv) > 3 else "admin@uit.edu.vn"
PASSW = sys.argv[4] if len(sys.argv) > 4 else "AdminUIT@2026"
CTF_NAME = "Seminar An toan thong tin - UIT"

# ---- Dinh nghia 2 challenge (file nam trong cung thu muc nay) ----
CHALLENGES = [
    {
        "folder": "cau2",
        "name": "Câu 1 - Truy tìm flag trong ảnh (Steganography)",
        "category": "Steganography",
        "description": ("Ảnh world cup chứa một thông điệp bí mật — một flag dạng UIT{...}. "
                        "Hoàn thành logic còn thiếu trong stego_tool.py để đọc file và lấy ra đáp án này."
                        "\n\nChạy: python stego_tool.py worldcup.png"),
        "value": 150,
        "flag": "UIT{h1dd3n_1n_pl41n_t3xt}",
        "hint": ("Làm cách nào đọc hết byte của file rồi tìm chuỗi UIT{...} trong đó? "
                 "Gợi ý: open(duong_dan, 'rb').read() để lấy byte, đổi sang text bằng "
                 ".decode('latin-1','ignore'), rồi re.search(r'UIT\\{[^}]+\\}', text)."),
        "files": ["worldcup.png", "stego_tool.py"],
    },
    {
        "folder": "cau3",
        "name": "Câu 2 - Vé VIP chung kết World Cup",
        "category": "Web Security",
        "description": ("WorldCup Ticket Box mở bán vé World Cup 2026. Vé thường ai cũng đặt được, "
                        "nhưng tấm vé VIP trận chung kết (in sẵn mã thưởng UIT{...}) chỉ dành cho admin. "
                        "Bạn đang vào với tư cách khách thường — không phải admin. Nghe nói trang này "
                        "xác định quyền admin khá hời hợt: nó tin vào đúng những gì trình duyệt của bạn "
                        "khai báo. Thử tìm cách trở thành admin để nhận vé VIP."
                        "\n\nhttps://web-production-57788.up.railway.app/"),
        "value": 200,
        "flag": "UIT{c00k1e_n0t_s4f3}",
        "hint": ("Mở F12 → Application → Cookies: server đang gán cookie role = 'user'. "
                 "Làm cách nào để trở thành 'admin'?"),
        "files": [],
    },
]

# Cac challenge do script nay quan ly: se XOA sach (theo ten) truoc khi tao lai,
# de chay nhieu lan van "dong bo" dung trang thai. Gom ca "Cau 1" da bo.
MANAGED_NAMES = {
    # --- ten cu (chi xoa cho sach neu instance con) ---
    "Câu 1 - Crack file ZIP có mật khẩu",                 # zip da bo
    "Câu 3 - Phân tích mã độc",                           # malware da bo
    "Câu 2 - Truy tìm flag trong ảnh (Steganography)",    # ten cu cua stego (truoc khi danh so lai)
    "Câu 3 - Khai thác Cookie web (Web Security)",        # ten cu cua web (truoc khi danh so lai)
    # --- ten hien tai (se xoa roi tao lai) ---
    "Câu 1 - Truy tìm flag trong ảnh (Steganography)",
    "Câu 2 - Khai thác Cookie web (Web Security)",    # ten truoc khi doi theme World Cup
    "Câu 2 - Vé VIP chung kết World Cup",
}

s = requests.Session()


def get_nonce(path):
    """Lay csrfNonce nhung trong 1 trang HTML cua CTFd."""
    r = s.get(BASE + path)
    m = re.search(r"'csrfNonce':\s*\"([0-9a-fA-F]+)\"", r.text) or \
        re.search(r'name="nonce"\s+value="([0-9a-fA-F]+)"', r.text)
    return m.group(1) if m else None


def do_setup():
    """Chay buoc /setup. Tra ve True neu da setup thanh cong / da setup tu truoc."""
    r = s.get(BASE + "/setup", allow_redirects=False)
    if r.status_code in (301, 302) and "setup" not in r.headers.get("Location", ""):
        print("[i] CTFd da duoc setup tu truoc -> dang dang nhap admin...")
        return login()
    nonce = get_nonce("/setup")
    if not nonce:
        print("[!] Khong lay duoc nonce o /setup (CTFd da setup roi?). Thu dang nhap...")
        return login()
    data = {
        "ctf_name": CTF_NAME,
        "ctf_description": "Cac thu thach Steganography va Web Security.",
        "user_mode": "users",
        "challenge_visibility": "private",
        "account_visibility": "public",
        "score_visibility": "public",
        "registration_visibility": "public",
        "verify_emails": "false",
        "name": ADMIN, "email": EMAIL, "password": PASSW,
        "ctf_theme": "core", "theme_color": "",
        "start": "", "end": "", "nonce": nonce,
    }
    r = s.post(BASE + "/setup", data=data, allow_redirects=False)
    if r.status_code in (200, 302):
        print(f"[OK] Da setup CTFd. Admin: {ADMIN} / {PASSW}")
        return True
    print(f"[!] Setup that bai (HTTP {r.status_code}).")
    return False


def login():
    nonce = get_nonce("/login")
    if not nonce:
        print("[!] Khong vao duoc trang /login.")
        return False
    r = s.post(BASE + "/login",
               data={"name": ADMIN, "password": PASSW, "nonce": nonce},
               allow_redirects=False)
    ok = r.status_code in (200, 302)
    print("[OK] Dang nhap admin." if ok else f"[!] Dang nhap that bai (HTTP {r.status_code}).")
    return ok


def api(method, path, nonce, **kw):
    headers = kw.pop("headers", {})
    headers["CSRF-Token"] = nonce
    return s.request(method, BASE + path, headers=headers, **kw)


def list_challenges(nonce):
    try:
        r = api("GET", "/api/v1/challenges?view=admin", nonce)
        return r.json().get("data", [])
    except Exception:
        return []


def delete_managed(nonce):
    """Xoa cac challenge do script quan ly (theo ten) de tao lai cho sach.
       Dong thoi loai bo 'Cau 1' cu vi no khong con trong CHALLENGES."""
    for c in list_challenges(nonce):
        if c.get("name") in MANAGED_NAMES:
            r = api("DELETE", f"/api/v1/challenges/{c['id']}", nonce)
            ok = r.status_code in (200, 204)
            try:
                ok = ok and r.json().get("success", True)
            except Exception:
                pass
            print(f"[-] {'Da xoa' if ok else 'Khong xoa duoc'} ban cu: {c['name']} (#{c['id']})")


def create_challenge(ch, nonce):
    r = api("POST", "/api/v1/challenges", nonce, json={
        "name": ch["name"], "category": ch["category"],
        "description": ch["description"], "value": ch["value"],
        "state": "visible", "type": "standard",
    })
    j = r.json()
    if not j.get("success"):
        print(f"[!] Tao challenge that bai: {ch['name']} -> {j}")
        return None
    cid = j["data"]["id"]
    print(f"[OK] Challenge #{cid}: {ch['name']}")

    # Flag
    api("POST", "/api/v1/flags", nonce, json={
        "challenge_id": cid, "content": ch["flag"], "type": "static", "data": ""})
    # Hint
    if ch.get("hint"):
        api("POST", "/api/v1/hints", nonce, json={
            "challenge_id": cid, "content": ch["hint"], "cost": 0, "type": "standard"})
    # Files
    for fn in ch["files"]:
        fp = os.path.join(HERE, ch["folder"], fn)
        with open(fp, "rb") as fh:
            # Voi multipart (khong phai JSON), CTFd kiem tra CSRF qua field 'nonce'
            rf = api("POST", "/api/v1/files", nonce,
                     data={"challenge_id": cid, "type": "challenge", "nonce": nonce},
                     files={"file": (fn, fh)})
        try:
            ok = rf.json().get("success")
        except Exception:
            ok = False
        print(f"       {'+' if ok else 'x'} file: {fn}")
        if not ok:
            print(f"         DEBUG http={rf.status_code} body={rf.text[:200]}")
    return cid


def main():
    print("=" * 60)
    print(f"  SEED CTFd: {BASE}")
    print("=" * 60)
    try:
        s.get(BASE + "/", timeout=5)
    except Exception as e:
        print(f"[!] Khong ket noi duoc CTFd tai {BASE}. CTFd da chay chua? ({e})")
        sys.exit(1)

    if not do_setup():
        sys.exit(1)
    nonce = get_nonce("/")
    if not nonce:
        print("[!] Khong lay duoc CSRF nonce sau dang nhap.")
        sys.exit(1)

    # 1) Don dep ban cu (gom ca Cau 1 da bo) roi 2) tao lai Cau 2 + Cau 3
    delete_managed(nonce)
    for ch in CHALLENGES:
        create_challenge(ch, nonce)

    print("=" * 60)
    print(f"  XONG! {len(CHALLENGES)} challenge (Cau 2 + Cau 3). Cau 1 da bo.")
    print(f"  Mo {BASE}  -> dang nhap/dang ky de lam bai.")
    print(f"  Admin: {ADMIN} / {PASSW}")
    print("=" * 60)


if __name__ == "__main__":
    main()
