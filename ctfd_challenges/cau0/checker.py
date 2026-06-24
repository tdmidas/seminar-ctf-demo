#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
checker.py -- Bộ kiểm tra flag cho câu Khởi động (Welcome).
============================================================================
Minh hoạ cách một hệ thống CTF "chấm" flag: lấy chuỗi thí sinh nộp, so sánh
với flag đúng. Khớp -> Correct (cộng điểm); không khớp -> Incorrect.

Chạy thử:
    python checker.py "UIT{welcome_to_uit_ctf}"   ->  Correct
    python checker.py "UIT{sai_flag}"             ->  Incorrect
    python checker.py                              ->  hỏi nhập flag
============================================================================
"""
import sys

# In tieng Viet / emoji ra console khong bi loi 'charmap' (Windows).
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Flag đúng của câu này (chỉ giáo viên / hệ thống biết).
FLAG = "UIT{welcome_to_uit_ctf}"


def check(submission):
    """Trả về True nếu flag thí sinh nộp khớp đúng flag của câu."""
    if not submission:
        return False
    return submission.strip() == FLAG


def main():
    submitted = sys.argv[1] if len(sys.argv) > 1 else input("Nhập flag: ")
    if check(submitted):
        print("✅ Correct! Flag hợp lệ — bạn đã biết cách nộp flag.")
        sys.exit(0)
    print("❌ Incorrect. Flag chưa đúng.")
    print("   Mẹo: copy đúng nguyên chuỗi UIT{...} (gồm cả 'UIT{' và '}').")
    sys.exit(1)


if __name__ == "__main__":
    main()
