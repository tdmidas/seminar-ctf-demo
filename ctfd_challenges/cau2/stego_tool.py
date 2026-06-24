#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
  Challenge 2 - Steganography Tool  (FILL IN THE BLANKS)
============================================================================

BACKGROUND: The file worldcup.png looks like an ordinary image, but the flag is
            hidden as plain TEXT inside the file itself (in the picture's
            metadata). The pixels look completely normal -- yet the flag is
            sitting right there in the bytes of the file.

            You do NOT need to touch the pixels. Just read the raw bytes of
            the file and look for the flag text  UIT{...} .

            Shortcut (no code): the classic `strings` command shows all the
            readable text in a file:
                strings worldcup.png                  (Linux / macOS)
                strings worldcup.png | findstr UIT     (Windows)

USAGE:
    python stego_tool.py worldcup.png

----------------------------------------------------------------------------
 YOUR TASK: implement the 2 blanks marked  >>> FILL <<< :
     (1) read_file_bytes() - read ALL the bytes of the image file
     (2) find_flag()       - locate the  UIT{...}  text inside those bytes
============================================================================
"""
import sys
import re


# ============================================================================
#  (1) >>> FILL <<<
#  Open the file in BINARY mode ("rb") and return ALL of its bytes.
# ============================================================================
def read_file_bytes(image_path):

    return data


# ============================================================================
#  (2) >>> FILL <<<
#  'data' is the raw bytes of the file. Find the flag  UIT{...}  hidden inside
#  it and return it as a string.
#  (Hint: turn the bytes into text, then search for the  UIT{...}  pattern.)
# ============================================================================
def find_flag(data):

    return flag


def main():
    image_path = sys.argv[1] if len(sys.argv) > 1 else "worldcup.png"
    print("=" * 56)
    print(f"  STEGO DECODER -- file: {image_path}")
    print("=" * 56)
    data = read_file_bytes(image_path)
    flag = find_flag(data)
    if flag and flag.startswith("UIT{"):
        print(f"  >>> FLAG FOUND: {flag}")
    else:
        print("  Flag not found. Check your two functions above.")
        print(f"  (Current result: {flag!r})")
    print("=" * 56)


if __name__ == "__main__":
    main()
